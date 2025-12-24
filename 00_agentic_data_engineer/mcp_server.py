from mcp.server.fastmcp import FastMCP
import chromadb
import chromadb.utils.embedding_functions

# 1. Initialize FastMCP
# This automatically creates the FastAPI app and SSE endpoint internally.
mcp = FastMCP("enterprise-crm")

# ---CONFIGURATIONS ---
DB_PATH = "./chroma_db"
COLLECTION_NAME = "company_policies"

# ---DATABASE CONNECTION (Read Only)---
try:
    client = chromadb.PersistentClient(path=DB_PATH)
    #We must use the same embedding function we used in the ingest script
    embed_fn = chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn
    )
    print(f"📚 Connected to Knowledge Base: {collection.count()} docs loaded.")

except Exception as e:
    print(f"⚠️ WARNING: Could not connect to Vector DB. Did you run ingest_knowledge.py? Error: {e}")
    collection = None

# --- DATABASE MOCK ---
orders_db = {
    "ORD-123": {"status": "shipped", "customer": "Sreeram", "total": 150.00},
}

# --- 2. DEFINE TOOLS ---
# ZERO GLUE CODE: We just write Python functions with Type Hints.
# FastMCP inspects 'order_id: str' and builds the tool definition automatically.

@mcp.tool()
def get_order(order_id: str) -> str:
    """Get the status and details of an order by ID."""
    order = orders_db.get(order_id)
    if not order:
        return "Order not found."
    return str(order)

@mcp.tool()
async def search_knowledge_base(query: str) -> str:
    """
    Searches the ingested internal documentation. 
    Use this tool IMMEDIATELY if the user asks about refunds, return policies, 
    or specific company guidelines. Do not answer from memory.
    """
    if not collection:
        return "Error: Knowledge base is offline."

    print(f"🔍 Vector Search for: '{query}'")
    
    # RAG: Retrieve Top 2 most relevant chunks
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    
    found_rules = results['documents'][0]
    
    if not found_rules:
        return "No relevant policy found."
    
    return "RELAVANT POLICY RULES:\n" + "\n- ".join(found_rules)

@mcp.tool()
def process_refund(order_id: str, reason: str) -> str:
    """Issue a refund. Requires order ID and a reason."""
    if order_id not in orders_db:
        return "Order not found."
    return f"Refund processed for {order_id}. Reason: {reason}"

# --- 3. RUN ---
if __name__ == "__main__":
    # This single line runs the Uvicorn server on port 8000
    mcp.run(transport='sse')
import chromadb
from chromadb.utils import embedding_functions

# --CONFIGURATIONS ---
DB_PATH = "./chroma_db"
COLLECTION_NAME = "company_policies"

def ingest_data():
    print("🚀 Starting Knowledge Ingestion...")

    # 1. Initialize Vector DB (persistent)
    client = chromadb.PersistentClient(path=DB_PATH)

    #2. Select Embedding Model (Runs locally on CPU/M4 Neural Engine)
    # This automatically handles tokenization and vectorization.
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    # 3. Create/Reset Collection
    # We delete existing data to ensure a fresh start (idempotency)
    print("Deleting existing collection...")
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Cleared old data.")
    except:
        pass # Collection doesn't exist yet

    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embed_fn)

    # 4. Raw Knowledge Base
    # In real life, you'd load these from PDF/Markdown files.ArithmeticError
    documents = [
        "Full refunds are only allowed if the item is 'lost_in_transit' or 'totally_destroyed'.",
        "Cosmetic damage (scratches/dents) is NOT eligible for a full refund.",
        "For cosmetic damage, a maximum of 10% partial refund is allowed. The customer must provide a photo.",
        "All refund requests must be made within 30 days of delivery.",
        "Electronics have a 1-year warranty for functional defects."
    ]

    # 5. Metadata (Optional but recomended for filtering)
    metadatas = [{"category": "refund_policy"} for _ in documents]
    ids = [f"policy_{i}" for i in range(len(documents))]

    # 6. Embed & Store
    print(f"🧠 Embedding {len(documents)} documents...")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ Success! Knowledge base saved to '{DB_PATH}'")

if __name__ == "__main__":
    ingest_data()    
    


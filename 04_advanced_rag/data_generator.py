import os
from arango import ArangoClient
from dotenv import load_dotenv

load_dotenv()

# Architect's Note: Use environment variables for credentials
ARANGO_URL = os.getenv("ARANGO_URL")
ARANGO_PWD = os.getenv("ARANGO_PASSWORD") # Maps to ARANGO_PASSWORD in .env

def setup_graph_data():
    if not ARANGO_URL or not ARANGO_PWD:
        print("❌ Error: ARANGO_URL and ARANGO_PASSWORD must be set in .env")
        return

    # 1. Initialize Client
    client = ArangoClient(hosts=ARANGO_URL)
    sys_db = client.db('_system', username='root', password=ARANGO_PWD)

    # 2. Create Database if not exists
    if not sys_db.has_database('glass_box'):
        sys_db.create_database('glass_box')
    
    db = client.db('glass_box', username='root', password=ARANGO_PWD)

    # 3. Setup Collections (Nodes and Edges)
    if not db.has_collection('kb_nodes'):
        db.create_collection('kb_nodes') # Vertex Collection
    if not db.has_collection('kb_edges'):
        db.create_collection('kb_edges', edge=True) # Edge Collection

    nodes = db.collection('kb_nodes')
    edges = db.collection('kb_edges')

    # 4. Generate the "Project Alpha" Knowledge Graph
    # We define clear hops: Person -> Project -> Service -> Protocol
    knowledge_nodes = [
        {"_key": "sreeram", "text": "Sreeram is the Lead Architect for Project Alpha."},
        {"_key": "proj_alpha", "text": "Project Alpha is a real-time agentic system for financial auditing."},
        {"_key": "svc_payments", "text": "The Payments Service handles all encrypted transactions for Alpha."},
        {"_key": "prot_iso27001", "text": "ISO27001 protocol mandates hardware-level encryption for payment services."}
    ]

    knowledge_edges = [
        {"_from": "kb_nodes/sreeram", "_to": "kb_nodes/proj_alpha", "label": "MANAGES"},
        {"_from": "kb_nodes/proj_alpha", "_to": "kb_nodes/svc_payments", "label": "DEPENDS_ON"},
        {"_from": "kb_nodes/svc_payments", "_to": "kb_nodes/prot_iso27001", "label": "GOVERNED_BY"}
    ]

    # 5. Clean and Insert
    nodes.truncate()
    edges.truncate()
    nodes.import_bulk(knowledge_nodes)
    edges.import_bulk(knowledge_edges)

    print(f"✅ 'Glass Box' Knowledge Graph populated in ArangoDB.")
    print(f"Nodes: {len(knowledge_nodes)} | Edges: {len(knowledge_edges)}")

if __name__ == "__main__":
    setup_graph_data()
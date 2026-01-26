# 🚀 Advanced RAG: Graph vs Vector Bakeoff

This module demonstrates the difference between **Vector RAG** (semantic similarity) and **Graph RAG** (structural reasoning) using ArangoDB.

## 📋 Prerequisites

### 1. ArangoDB Setup (Version 3.12+)
> [!IMPORTANT]
> This project requires **ArangoDB 3.12 or higher** for native Vector Search capabilities.

Run ArangoDB using Docker:
```bash
docker run -e ARANGO_ROOT_PASSWORD=somepassword -p 8529:8529 -d --name arangodb arangodb
```

### 2. Environment Configuration
Create a `.env` file in the project root (or within this folder) with the following variables:
```env
ARANGO_URL=http://localhost:8529
ARANGO_PASSWORD=somepassword
OPENAI_API_KEY=your_openai_api_key
```

## 🏗️ Getting Started

### Step 1: Populate the Knowledge Graph
Run the `data_generator.py` script to initialize the `glass_box` database and populate it with a sample knowledge graph (Project Alpha).

```bash
python data_generator.py
```
This script creates:
- **Nodes (`kb_nodes`):** Persons, Projects, Services, and Protocols.
- **Edges (`kb_edges`):** Relationships like `MANAGES`, `DEPENDS_ON`, and `GOVERNED_BY`.

### Step 2: The GraphRAG Bakeoff
Open and run the `graph_rag_bakeoff.ipynb` notebook. It walks through:
1. **Semantic Search View:** Creating an ArangoSearch View for vector indexing.
2. **Vector RAG:** A standard similarity search that often misses deeply linked context.
3. **Graph RAG:** Using AQL (ArangoDB Query Language) to traverse relationships and bridge the "Reasoning Gap."

## 🧠 Why GraphRAG?
While Vector Search is great for finding the "nearest" text, it is blind to structure. GraphRAG follows the **edges** to find context that is logically connected but semantically different (e.g., finding a security protocol linked to a service managed by a specific architect).

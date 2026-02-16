# 🛠️ Week 6: Multi-Hop Reasoning with GraphRAG

This module explores the integration of professional-grade tools and the **Model Context Protocol (MCP)** to enhance agent capabilities. We transition from basic retrieval to **Multi-Hop Retrieval** and **Entity Resolution** within a graph-based knowledge system.

## 🧠 Key Concepts

### 1. Model Context Protocol (MCP)
MCP is an open standard that enables AI models to securely and consistently access data and tools across different platforms. We focus on building and consuming MCP servers to extend our agent's reach.

### 2. Multi-Hop Graph RAG
Unlike single-step vector retrieval, Multi-Hop RAG traverses relationships in the knowledge graph (ArangoDB) to answer complex questions that require connecting multiple pieces of information (e.g., "Find the manager of the person who reported the security incident").

### 3. Entity Resolution
This process involves identifying and merging duplicate or related entities within the graph to maintain a "Single Source of Truth," ensuring the agent doesn't get confused by fragmented data.

## 📂 Notebooks

- **[MultiHop_GraphRAG_Entity_Resolution.ipynb](MultiHop_GraphRAG_Entity_Resolution.ipynb)**: Advanced implementation of multi-hop traversal and entity deduplication logic.

## 🏗️ Getting Started

### Prerequisites
1. **ArangoDB 3.12+**: Ensure your instance is running (preferably via Docker as shown in [Week 4](../04_advanced_rag/README.md)).
2. **Environment Variables**: A `.env` file with `ARANGO_URL`, `ARANGO_PASSWORD`, and `OPENAI_API_KEY` (Refer to [Week 5](../05_agent_orchestration/README.md) for details).

## 🛠️ Data Infrastructure
This module builds upon the `glass_box` database. Ensure the data generator from previous weeks has been executed to populate the base knowledge graph.

# 🛠️ Week 6: Multi-Hop Reasoning with GraphRAG

## 🧠 The Problem: Contextual Blindness
Most internal AI initiatives fail because they treat enterprise knowledge as a stack of disconnected pages. This leads to **Contextual Drift**—where the AI loses the logical "thread" connecting a Slack conversation to a Jira ticket and its final GitHub commit. 

This repository provides the framework to bridge that **"Semantic Gap"** using a deterministic reasoning engine.

---

## 🛠️ Repository Architecture

### 1. The Reasoning Substrate (ArangoDB)
We use **ArangoDB** to solve the "Missing Middle" between raw data and LLM logic.
* **Entity Resolution (ER):** Normalizing siloed aliases (e.g., `@Sreeram` on Slack vs `snudurupati` on Jira) into a unified Global Entity ID.
* **Semantic Bridges:** Edge collections that define the logical "verbs" connecting disparate data points.
* **Multi-Hop Pathfinder:** AQL-driven traversals that "walk" the graph from intent to technical resolution.

### 2. The Gap Detector
An agentic node built with **LangGraph** that proactively identifies **Stalled Work**—tasks marked "In Progress" in management tools that show zero activity in the codebase.

---

## 🚀 Quick Start

### 1. Configure the Substrate
Connect to your ArangoDB instance and initialize the "Corporate Brain" schema.

```bash
# Clone the repository
git clone [https://github.com/](https://github.com/)[your-username]/corporate-brain-week-6.git
cd corporate-brain-week-6

# Install dependencies
pip install -r requirements.txt

### Prerequisites
1. **ArangoDB 3.12+**: Ensure your instance is running (preferably via Docker as shown in [Week 4](../04_advanced_rag/README.md)).
2. **Environment Variables**: A `.env` file with `ARANGO_URL`, `ARANGO_PASSWORD`, and `OPENAI_API_KEY` (Refer to [Week 5](../05_agent_orchestration/README.md) for details).

## 🛠️ Data Infrastructure
This module builds upon the `glass_box` database. Ensure the data generator from previous weeks has been executed to populate the base knowledge graph.

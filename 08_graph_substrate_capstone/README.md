# 🏆 Week 8: The "Missing Middle" Showdown (CPT vs. GraphRAG)

Welcome to the finale of this 8-week series. This repository contains the construction logic and evaluation framework for comparing **Continued Pre-training (CPT)** against **Graph-Augmented Retrieval (GraphRAG)**. 

In this capstone, we move beyond "stochastic" predictions to build a **Clinical Knowledge Substrate** capable of 100% factual traceability on local Apple Silicon (M4) infrastructure.

## 📑 8-Week Series Roadmap
This project is the culmination of a step-by-step evolution from Data Engineering to **Context Engineering**:
| Week | Topic | Key Concepts |
|------|-------|--------------|
| **[Week 0](./00_agentic_data_engineer)** | **The Agentic Data Engineer** | *The original demo. How to start thinking like an agent.* |
| **[Week 1](./01_stochastic_cpu)** | **The Stochastic CPU** | Latency, tokens, and the "new compute" mindset. |
| **[Week 2](./02_structured_output)** | **Structured Output** | Making LLMs deterministic with Pydantic. |
| **[Week 3](./03_rag_fundamentals)** | **RAG Fundamentals** | Vector databases, embeddings, and semantic search. |
| **[Week 4](./04_advanced_rag)** | **Advanced RAG** | Hybrid search, re-ranking, and overcoming retrieval failures. |
| **[Week 5](./05_agent_orchestration)** | **Agent Orchestration** | Moving from chains to state machines (LangGraph). |
| **[Week 6](./06_multi_hop_reasoning_GraphRAG)** | **Multi-Hop Reasoning with GraphRAG** | Entity Resolution, Semantic Bridging and Explainable AI. |
| **[Week 7](./07_continued_pre_training)** | **Continued Pre-Training** | Testing the untestable: LLM-as-a-judge and tracing. |
| **[Week 8](./08_graph_substrate_capstone)** | **The Showdown** | CPT vs. GraphRAG Head-to-Head. |

---

## 🔬 The "Multi-Hop" Acid Test
We pitted our **Week 7 Parametric Contender** (Llama-3-8B with specialized weights) against our **Week 8 Semantic Contender** (Base Llama-3-8B + Memgraph Substrate).

**The Query:** *"In our records, what role does the 'forearm' play in measuring glucose uptake for hypertensive subjects?"*

| Model | Result | Verdict |
| :--- | :--- | :--- |
| **Week 7 CPT** | `"Data not found in substrate."` | **Failed:** The rare, high-specificity relationship was "smeared" during training. |
| **Week 8 GraphRAG** | `"The forearm is the site where glucose uptake was measured..."` | **Winner:** Preserved the low-frequency "long-tail" facts with 100% fidelity. |



---

## 🛠️ Tech Stack & Infrastructure
* **LLM:** Meta-Llama-3-8B-Instruct (4-bit quantized).
* **Inference Engine:** `mlx-lm` (Optimized for Apple Silicon).
* **Graph Database:** Memgraph (Property Graph via Bolt protocol).
* **Orchestration:** Python 3.11+.
* **Key Libraries:** `neo4j` (Driver), `networkx`, `pydantic`.

---

## 🚀 Project Structure

### 1. Substrate Construction
The first phase involves ingesting 3,508 clinical abstracts into Memgraph.
* **Entity Resolution:** Normalizes clinical terms (e.g., *Hypertension*) to ensure "knowledge duplicates" are merged into single hub nodes.
* **Semantic Bridging:** Materializes `CO_OCCURS_WITH` relationships, allowing the LLM to traverse concepts that aren't in the same sentence.

### 2. The Showdown
We run a standardized, zero-temperature inference to compare the specialized weights of the CPT model against the grounded context of the GraphRAG substrate.

---

## 📈 The Architect's Verdict
For enterprise applications where "mostly right" is "totally wrong," **Architecture > Weights**.
* **CPT** provides **Fluency**: It excels at specialized vocabulary and domain-specific tone.
* **GraphRAG** provides **Fidelity**: It preserves exact relationships and offers a 100% auditable decision path.



## 🔮 What's Next?
This concludes the 8-week series on becoming an AI Architect. Stay tuned for my next series, where I combine **Streaming** and **Context Engineering** to build a real-time context engine.

**🔗 Full Results & Blog Post:** [[Link to Substack](https://www.nudurupati.co/)]
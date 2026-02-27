# 🧠 Week 7: The Parametric Layer & Continuous Pre-training (CPT)

## 🏗️ Architectural Overview
This folder contains the **"Clinical Contender"** experiment. The goal of Week 7 was to investigate the **Parametric Layer** of a Large Language Model—specifically, whether we can solve the "Missing Middle" problem by baking domain-specific knowledge directly into a model's weights.

We performed **Continuous Pre-training (CPT)** on a commodity Llama-3-8B model using specialized neurological clinical data, optimized for local execution on **Apple Silicon (M4)**.

## 🔬 The Experiment: "The Clinical Contender"
We pitted a "Vanilla" Llama-3-8B against a version specialized via **QLoRA** (Quantized Low-Rank Adaptation). 

### 🛠️ Technical Stack
- **Hardware:** MacBook Air M4 (24GB Unified Memory)
- **Framework:** [Apple MLX](https://github.com/ml-explore/mlx) (Native Apple Silicon Optimization)
- **Base Model:** `Llama-3-8B-Instruct-4bit`
- **Dataset:** Medical Text Condition Classification (Kaggle) mixed with WikiText-2 (Replay Buffer).

## 📂 Folder Structure
* `AI_Architect_Series_W7_CPT_The_Clinical_Contender.ipynb`: The "Glass Box" notebook containing the ETL pipeline, Tokenization Audit, and Training Loop.
* `config.yaml`: The MLX-LM training configuration optimized for fanless thermal profiles.
* `data/`: (Generated) Contains the `train.jsonl` substrate used for training.
* `adapters.safetensors/`: (Generated) The final parametric "delta" representing the specialized neurological knowledge.

## 📈 Key Findings
1. **Conceptual Density:** The model's accuracy on technical medical definitions (e.g., TIA durations and Oligodendrocyte function) increased significantly.
2. **Linguistic Drift:** Without an instruction-tuning phase following CPT, the model experienced "persona decay," leading to repetitive `<|eot_id|>` tokens and a loss of conversational formatting.
3. **The Semantic Gap:** While the model became a "Medical Specialist," it failed to bridge the gap between technical signals (Sensor Drift) and operational impact (Jira Blockers). 

## ⚖️ Conclusion for the AI Architect
Continuous Pre-training is a powerful tool for **Vocabulary Expansion** and **Domain Adaptation**, but it is "brittle." It modifies the *how* of the model's thinking without necessarily improving the *connections* between disparate data points.

---
**Next Step:** [Week 8] — The Knowledge Graph Showdown. We will pit this **Clinical Contender** against a **GraphRAG** architecture to see which can truly solve the "Missing Middle."
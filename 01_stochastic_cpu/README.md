# Week 1: The Stochastic CPU 🧠⚡️

Welcome to Week 1 of the **Agentic AI Architect** curriculum! This week, we pivot from traditional, deterministic computing to the world of **Stochastic Computing**.

## 🧠 What is a "Stochastic CPU"?

In traditional software engineering, if you call a function `add(2, 2)`, you expect `4` every single time, with near-zero latency. In the world of LLMs, the model is a **Stochastic CPU**:
- **Non-deterministic**: The same prompt can yield different outputs.
- **Latency-bound**: Output is produced token-by-token, making time-to-first-token (TTFT) and throughput (tokens/sec) critical metrics.
- **Token-based Cost**: You don't pay for "compute hours" in the same way; you pay for "tokens" consumed and generated.

## 📊 The LLM Benchmark Script

In this folder, you'll find `llm_benchmark.py`. This script is designed to help you understand the performance and cost trade-offs between different LLM providers (specifically OpenAI and local Ollama instances).

### Key Metrics Tracked:
- **Latency**: The total time taken to generate the response.
- **Throughput**: How many tokens are generated per second.
- **Input/Output Tokens**: The volume of data processed.
- **Cost (USD)**: Real-time cost calculation based on current pricing models.

---

## 🚀 Setup & Usage

### 1. Prerequisite: Ollama
Ensure you have [Ollama](https://ollama.com/) installed and the `gpt-oss:20b` (or your preferred) model pulled.
```bash
ollama pull gpt-oss:20b
```

### 2. Prepare Environment
We recommend using the virtual environment created during the initial setup.
```bash
source .venv/bin/activate
```

### 3. Configure API Keys
Copy the `.env.example` file from the root directory and add your OpenAI API key:
```bash
cp ../.env.example .env
# Edit .env with your key
```

### 4. Run the Benchmark
```bash
python3 llm_benchmark.py
```

## 📈 Example Output
The script will generate a clean comparison table:

```text
+--------------+----------------+-----------+--------------+----------------+-----------------+-------------+--------------+---------------+------------+
| model_name   | api_provider   |   latency |   throughput |   input_tokens |   output_tokens |   eval_rate |   input_cost |   output_cost |   cost_usd |
+==============+================+===========+==============+================+=================+=============+==============+===============+============+
| gpt-4o       | openai         |   1.60538 |            1 |            219 |             135 |    220.509  |    0.0005475 |    0.00016875 | 0.00071625 |
+--------------+----------------+-----------+--------------+----------------+-----------------+-------------+--------------+---------------+------------+
| gpt-oss:20b  | ollama         |  15.7816  |            1 |            279 |             384 |     24.3321 |    0         |    0          | 0          |
+--------------+----------------+-----------+--------------+----------------+-----------------+-------------+--------------+---------------+------------+
```

---

## 🎯 Learning Objectives
1. Understand the difference between TTFT and full-stream latency.
2. Develop a "cost-conscious" mindset when choosing between proprietary and open-source models.
3. Learn to handle non-determinism in your "LLM(Stochastic CPU)" calls.

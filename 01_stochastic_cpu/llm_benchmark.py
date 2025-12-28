import time
import ollama
import os
from tabulate import tabulate
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# 1. Define structured data model for the benchmark results
class LLMBenchmarkResult(BaseModel):
    model_name: str
    api_provider: str
    latency: float
    throughput: float
    input_tokens: int
    output_tokens: int
    eval_rate: float
    input_cost: float
    output_cost: float
    cost_usd: float

# 2. Define the LLM benchmark functions

def benchmark_openai(prompt: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    start_ts = time.time()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    end_ts = time.time()
    input_tokens=response.usage.prompt_tokens
    output_tokens=response.usage.completion_tokens
    input_cost = (input_tokens / 1_000_000) * 2.50
    output_cost = (output_tokens / 1_000_000) * 1.25

    # GPT-4o costs $2.50 per 1M input tokens and $1.25 per 1M output tokens
    return LLMBenchmarkResult(
        model_name="gpt-4o",
        api_provider="openai",
        latency=end_ts - start_ts,
        throughput=1,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        eval_rate=response.usage.total_tokens / (end_ts - start_ts),
        input_cost=input_cost,
        output_cost=output_cost,
        cost_usd=input_cost + output_cost
    )

def benchmark_ollama(prompt: str):
    client = ollama
    start_ts = time.time()
    response = client.chat(
        model="gpt-oss:20b",
        messages=[{"role": "user", "content": prompt}]
    )
    end_ts = time.time()
    # gpt-oss:20b, running within ollama on your local machine costs $0 per 1M tokens
    return LLMBenchmarkResult(
        model_name="gpt-oss:20b",
        api_provider="ollama",
        latency=end_ts - start_ts,
        throughput=1,
        input_tokens=getattr(response, 'prompt_eval_count', 0),
        output_tokens=getattr(response, 'eval_count', 0),
        eval_rate=getattr(response, 'eval_count', 0) / (end_ts - start_ts), 
        input_cost=0.0,
        output_cost=0.0,
        cost_usd=0.0
    )   

# 3. Run the LLM benchmark functions
prompt = """Summarize this Anthropic blog post:
                As model capabilities improve, we can now build general-purpose agents that interact with full-fledged computing environments. Claude Code, for example, can accomplish complex tasks across domains using local code execution and filesystems. But as these agents become more powerful, we need more composable, scalable, and portable ways to equip them with domain-specific expertise.

                This led us to create Agent Skills: organized folders of instructions, scripts, and resources that agents can discover and load dynamically to perform better at specific tasks. Skills extend Claude’s capabilities by packaging your expertise into composable resources for Claude, transforming general-purpose agents into specialized agents that fit your needs.

                Building a skill for an agent is like putting together an onboarding guide for a new hire. Instead of building fragmented, custom-designed agents for each use case, anyone can now specialize their agents with composable capabilities by capturing and sharing their procedural knowledge. In this article, we explain what Skills are, show how they work, and share best practices for building your own.
                """
results = []


try:
    openai_result = benchmark_openai(prompt)
    results.append(openai_result)
except Exception as e:
    print(f"Skipping OpenAI benchmark: {e}")

try:
    ollama_result = benchmark_ollama(prompt)
    results.append(ollama_result)
except Exception as e:
    print(f"Skipping Ollama benchmark: {e}")

# 4. Tabulate and print the results
data = [result.model_dump() for result in results]
print(tabulate(data, headers="keys", tablefmt="psql"))

    


import logging
import os

from typing import List
from email_analyzer import EmailClassifier, EmailAnalysis
from langchain_classic.evaluation import load_evaluator
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. Setup Logging for observability (Week 7 Core Concept)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# 2. Define the Test Suite ("Golden Dataset" - 10+ examples including edge cases)
test_suite = [
    {"text": "My login doesn't work and you guys also overcharged me $50!", "ref": "technical_support"}, # Ambiguous
    {"text": "Wow, what a great service. It only crashes every five minutes. Amazing.", "ref": "complaint"}, # Passive-aggressive
    {"text": "No puedo acceder a mi cuenta desde ayer por la tarde.", "ref": "technical_support"}, # Multilingual
    {"text": "I'm interested in buying 500 licenses for my enterprise team.", "ref": "sales"}, # Sales
    {"text": "Your UI is ugly and I hate the new update.", "ref": "complaint"}, # Complaint
    {"text": "Click here for a $500 Amazon Gift Card!!!", "ref": "spam"}, # Spam
    {"text": "Where can I download my invoice for October?", "ref": "billing"}, # Billing
    {"text": "Is there an API endpoint for bulk user export?", "ref": "technical_support"}, # Technical support
    {"text": "I'm leaving for a competitor because your support is slow.", "ref": "complaint"}, # Complaint
    {"text": "Can you extend my trial by another 14 days?", "ref": "sales"}, # Sales
]

def run_evaluation_suite(logs: List[dict]):
    """Implementation of LLM-as-Judge"""
    print("\n" + "="*50)
    print("STARTING PROGRAMMATIC EVALUATION")
    print("="*50)
    
    # Use a high-capability model (GPT-4) to judge the classifier
    evaluator = load_evaluator("labeled_criteria", criteria="correctness", llm=ChatOpenAI(model="gpt-4o", temperature=0))
    
    for entry in logs:
        eval_result = evaluator.evaluate_strings(
            prediction=entry["prediction"],
            reference=entry["reference"],
            input=entry["input"]
        )
        
        status = "✅ PASS" if eval_result["score"] >= 0.5 else "❌ FAIL"
        print(f"\nInput: {entry['input'][:60]}...")
        print(f"Result: {entry['prediction']} (Ref: {entry['reference']}) | {status}")
        print(f"Reasoning: {eval_result['reasoning']}")

def main():
    # Initialize the reusable classifier module
    # Note: Prompt is loaded from version-controlled classifier_prompt.yaml
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "classifier_prompt.yaml")
    classifier = EmailClassifier(prompt_path=prompt_path)
    
    classification_logs = []

    print("="*50)
    print("STARTING EMAIL CLASSIFICATION BATCH")
    print("="*50)

    for example in test_suite:
        try:
            # Execute classification with built-in validation (confidence < 0.7)
            result: EmailAnalysis = classifier.classify(example["text"])
            
            # Log results for later programmatic evaluation
            classification_logs.append({
                "input": example["text"],
                "prediction": result.category,
                "reference": example["ref"],
                "confidence": result.confidence
            })
            
            print(f"Processed: {result.category} (Confidence: {result.confidence})")
            
        except Exception as e:
            logging.error(f"Failed to process email: {e}")

    # Run the Eval Suite using the LLM-as-Judge pattern
    run_evaluation_suite(classification_logs)

if __name__ == "__main__":

    main()
import logging
from typing import Literal, List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import load_prompt, ChatPromptTemplate

# 1. Define the Data Contract (Architectural Schema)
class EmailAnalysis(BaseModel):
    category: Literal["billing", "technical_support", "sales", "complaint", "spam"] = Field(
        description="The primary intent of the email."
    )
    priority: Literal["high", "medium", "low"]
    summary: str = Field(description="A concise 1-sentence summary.")
    confidence: float = Field(ge=0, le=1, description="Confidence score 0.0 to 1.0.")

class EmailClassifier:
    def __init__(self, prompt_path: str, model_name: str = "gpt-4o"):
        self.parser = PydanticOutputParser(pydantic_object=EmailAnalysis)
        self.model = ChatOpenAI(model=model_name, temperature=0.0) # Ensure determinism
        self.logs = []

        # 2. Structured Prompt: Context, Clarity, Structure, Iteration
        # Load the version-controlled prompt from the YAML file
        self.loaded_system_prompt = load_prompt(prompt_path)

    def classify(self, email_text: str, max_retries: int = 1) -> EmailAnalysis:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.loaded_system_prompt.template),
            ("user", "Email content: {email_text}")
        ])
        
        # 3. Classification Loop and Logging
        chain = prompt | self.model | self.parser
        
        for attempt in range(max_retries + 1):
            try:
                result = chain.invoke({
                    "email_text": email_text,
                    "format_instructions": self.parser.get_format_instructions()
                })
                
                # 3. Validation Logic
                if result.confidence < 0.7:
                    logging.warning(f"Low confidence ({result.confidence}) for email. Retrying...")
                    if attempt < max_retries: continue
                
                # Log for Week 3 Evaluation
                self.logs.append({"input": email_text, "output": result.model_dump()})
                return result
                
            except Exception as e:
                logging.error(f"Classification failed on attempt {attempt}: {e}")
                if attempt == max_retries:
                    raise e
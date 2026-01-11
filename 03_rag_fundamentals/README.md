# Week 3: RAG Fundamentals

This folder contains the materials for Week 3, focusing on the fundamentals of Retrieval Augmented Generation (RAG).

## Contents

- `week_3_rag_etl_pipeline.ipynb`: A Jupyter notebook demonstrating the RAG "ETL" pipeline:
  - **EXTRACT**: Loading raw PDF data using `PyMuPDFLoader`.
  - **TRANSFORM**: Chunking text into semantic windows using `RecursiveCharacterTextSplitter`.
  - **LOAD**: Embedding and storing vectors (to be implemented).

## Key Concepts

- Glass Box RAG: Understanding RAG as a data engineering pipeline rather than a "black box".
- PDF Extraction: Using robust loaders like `pymupdf` to handle diverse documents.
- Semantic Chunking: Breaking down large documents into manageable, context-rich pieces for better retrieval.

## Setup

Ensure you have the latest dependencies installed:
```bash
pip install -r ../requirements.txt
```

## Running the Notebook

To run the notebook locally, follow these steps:

1. **Set your OpenAI API Key:**
   ```bash
   export OPENAI_API_KEY=sk-proj-your-key
   ```

2. **Navigate to the folder:**
   ```bash
   cd 03_rag_fundamentals
   ```

3. **Launch the notebook:**
   ```bash
   jupyter notebook week_3_rag_etl_pipeline.ipynb
   ```

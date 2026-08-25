# Production RAG System

A production-oriented Retrieval-Augmented Generation (RAG) system built with Python, FAISS, sentence-transformer embeddings, Gemini, and FastAPI.

The system loads a PDF knowledge base, chunks the documents, generates embeddings, stores them in FAISS, retrieves the most relevant chunks for a user query, and generates a grounded answer using Gemini.

## Architecture

```text
PDF Document
     ↓
Document Loader
     ↓
Text Chunking
     ↓
Embedding Model
     ↓
FAISS Vector Index
     ↓
Retriever
     ↓
Top-K Relevant Chunks
     ↓
Prompt Construction
     ↓
Gemini LLM
     ↓
Grounded Answer + Sources
     ↓
FastAPI

RAG-Production-Project/
│
├── data/
│   └── Rag_llm.pdf
│
├── evaluation/
│   ├── __init__.py
│   ├── evaluate_answers.py
│   ├── evaluate_faithfulness.py
│   ├── evaluate_retrieval.py
│   └── questions.json
│
├── src/
│   ├── api/
│   │   ├── main.py
│   │   └── schemas.py
│   │
│   ├── chunking/
│   │   └── chunker.py
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── ingestion/
│   │   ├── index.py
│   │   └── loader.py
│   │
│   ├── llm/
│   │   └── llm_client.py
│   │
│   ├── prompts/
│   │   └── prompt_templates.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── utils/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logger.py
│   │
│   ├── vectordb/
│   │   └── vector_store.py
│   │
│   └── rag_pipeline.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_rag.py
│   └── test_retriever.py
│
├── .env
├── .gitignore
├── config.yaml
├── main.py
├── requirements.txt
├── README.md
└── test_retrieval.py

## Technologies

- Python
- FastAPI
- FAISS
- Sentence Transformers
- Gemini
- Pytest
- Uvicorn

## RAG Pipeline

### 1. Document Ingestion

The source PDF is loaded and processed into smaller document chunks.

Current knowledge base:

- 21 PDF pages
- 136 chunks

### 2. Embeddings

Each document chunk is converted into a vector representation using the configured embedding model.

Current embedding dimension:

```text
384
```

### 3. Vector Database

FAISS is used for efficient vector similarity search.

The generated FAISS index is stored locally and excluded from Git because it can be regenerated from the source document.

### 4. Retrieval

The retriever converts the user's question into an embedding and searches the FAISS index for relevant chunks.

The current production configuration uses:

```text
Top K = 4
```

Top K was evaluated using values of 3, 4, and 5.

| Top K | Average Precision | Average Recall |
|------:|------------------:|---------------:|
| 3 | 46.67% | 80.00% |
| 4 | 45.00% | 100.00% |
| 5 | 39.67% | 100.00% |

Top K = 4 was selected because it maintains 100% recall while providing better precision than Top K = 5 and limiting the amount of context passed to the LLM.

### 5. Generation

The retrieved document chunks are passed to Gemini through the RAG prompt.

The generated response contains the answer along with source page information and retrieval scores.

## API

The application exposes a FastAPI interface.

Start the server:

```bash
uvicorn src.api.main:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

### Interactive API Documentation

FastAPI automatically provides Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "rag-api"
}
```

### Query

```http
POST /query
```

Request:

```json
{
  "question": "What are the main challenges of RAG?"
}
```

The response contains:

- User question
- Generated answer
- Retrieved source pages
- Retrieval scores

Example structure:

```json
{
  "question": "What are the main challenges of RAG?",
  "answer": "Based on the provided context...",
  "sources": [
    {
      "page": "1",
      "score": 0.7454
    },
    {
      "page": "2",
      "score": 0.7144
    },
    {
      "page": "14",
      "score": 0.7021
    },
    {
      "page": "3",
      "score": 0.6909
    }
  ]
}
```

## Validation and Error Handling

The API validates incoming questions.

An empty question is rejected with a validation error.

Example:

```json
{
  "question": ""
}
```

The API returns a validation response instead of processing an invalid request.

The project also uses custom exceptions for RAG and retrieval failures.

## Testing

The project contains automated tests covering:

- API health checks
- API input validation
- Successful API queries
- RAG pipeline behavior
- Empty-question handling
- Retriever behavior
- Retriever failure handling

Run the complete test suite:

```bash
pytest -v
```

Current result:

```text
9 passed
```

## Retrieval Evaluation

Retrieval quality can be evaluated using:

```bash
python -m evaluation.evaluate_retrieval
```

The evaluation contains five questions with expected source pages.

Current baseline:

```text
Retrieval Hit Rate: 100.00%
Average Precision@4: 45.00%
Average Recall@4: 100.00%
Questions Evaluated: 5
```

The evaluation questions and expected pages are defined in:

```text
evaluation/questions.json
```

## Answer Evaluation

Generated answers can be evaluated using:

```bash
python -m evaluation.evaluate_answers
```

The evaluation checks whether the RAG pipeline successfully generates answers for the evaluation questions.

Current baseline:

```text
Answer Generation Rate: 100.00%
Questions Evaluated: 5
```

## Faithfulness Evaluation

The project also includes a faithfulness evaluation script:

```bash
python -m evaluation.evaluate_faithfulness
```

This evaluates whether generated answers are supported by the retrieved context.

Initial baseline:

```text
Faithfulness Score: 100.00%
Questions Successfully Evaluated: 4/4
```

One additional evaluation could not be completed because the Gemini API quota was exhausted during that run.

Therefore, this result should be treated as an initial baseline rather than a statistically significant benchmark.

## Configuration

Application configuration is stored in:

```text
config.yaml
```

Sensitive credentials such as the Gemini API key are stored in:

```text
.env
```

The `.env` file is excluded from Git.

Do not commit API keys or other credentials to the repository.

## Environment Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file containing the required API credentials.

## Build the Vector Index

After adding or modifying the source documents, rebuild the FAISS index:

```bash
python -m src.ingestion.index
```

The indexing pipeline performs:

```text
Load PDF
   ↓
Create Chunks
   ↓
Generate Embeddings
   ↓
Build FAISS Index
   ↓
Save Index
```

Current indexing result:

```text
Pages loaded: 21
Chunks created: 136
Embedding dimension: 384
FAISS vectors: 136
```

## Running the Complete System

### Terminal 1: Start the API

```powershell
uvicorn src.api.main:app --reload
```

### Terminal 2: Query the API

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/query" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"question":"What are the main challenges of RAG?"}'
```

### Run Tests

```powershell
pytest -v
```

### Run Retrieval Evaluation

```powershell
python -m evaluation.evaluate_retrieval
```

## Logging

The application uses centralized logging through the utility logging module.

Logs are written to the local `logs/` directory.

Log files are excluded from Git.

## Security

The project follows basic secret-management practices:

- API keys are stored in `.env`
- `.env` is excluded from Git
- Virtual environments are excluded from Git
- Generated indexes are excluded from Git
- Python cache files are excluded from Git
- Logs are excluded from Git

## Production-Oriented Features

The project includes:

- Modular RAG architecture
- PDF document ingestion
- Configurable chunking
- Embedding generation
- FAISS vector search
- Configurable Top K retrieval
- Gemini LLM integration
- Grounded answer generation
- Source attribution
- FastAPI REST API
- Request validation
- Custom exception handling
- Centralized logging
- Automated testing
- Retrieval evaluation
- Answer generation evaluation
- Faithfulness evaluation
- Environment-based secret management

## Current Project Status

```text
Document ingestion        ✅
Chunking                   ✅
Embeddings                ✅
FAISS indexing             ✅
Retrieval                  ✅
Gemini generation          ✅
FastAPI                    ✅
Input validation           ✅
Logging                    ✅
Exception handling         ✅
Automated tests            ✅ 9/9
Retrieval Hit Rate         ✅ 100%
Recall@4                   ✅ 100%
Precision@4                ⚠️ 45%
Answer Generation Rate     ✅ 100%
Faithfulness Baseline      ✅ 100% on 4/4 evaluated
Top K                      ✅ 4
```

## Future Improvements

Potential future improvements include:

- Hybrid keyword + vector retrieval
- Cross-encoder reranking
- Query rewriting
- Better chunking strategies
- Larger evaluation datasets
- Automated faithfulness benchmarking
- Response latency monitoring
- Retrieval observability
- Authentication and authorization
- Containerized deployment
- Cloud deployment
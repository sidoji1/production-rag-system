# RAG Explorer

A production-oriented Retrieval-Augmented Generation (RAG) system built with Python, FAISS, Sentence Transformers, Gemini, FastAPI, and React.

RAG Explorer allows users to ask questions about a PDF knowledge base through a web interface. The system retrieves relevant document chunks using semantic search and generates grounded answers using Gemini.

---

## Features

- PDF document ingestion
- Configurable text chunking
- Sentence Transformer embeddings
- FAISS vector similarity search
- Top-K document retrieval
- Gemini-powered answer generation
- Grounded answers using retrieved context
- Source page attribution
- Similarity scores for retrieved documents
- FastAPI REST API
- React + Vite frontend
- CORS support for frontend/backend communication
- Input validation and error handling
- Structured application logging
- Automated unit and API tests
- Retrieval evaluation
- Answer generation evaluation
- Retrieval Precision@K and Recall@K evaluation
- Clean and minimal web interface

---

## Architecture

```text
                         RAG Explorer
                              |
                    React + Vite Frontend
                              |
                         FastAPI API
                              |
                         RAG Pipeline
                              |
                +-------------+-------------+
                |                           |
            Retriever                    Prompt
                |                           |
             FAISS                         |
                |                           |
       Relevant document chunks             |
                +-------------+-------------+
                              |
                         Gemini LLM
                              |
                    Grounded Answer
                              |
                    Answer + Sources
```

---

## RAG Pipeline

```text
PDF Document
     |
     v
Document Loader
     |
     v
Text Chunking
     |
     v
Embedding Model
     |
     v
FAISS Vector Index
     |
     v
Retriever
     |
     v
Top-K Relevant Chunks
     |
     v
Prompt Construction
     |
     v
Gemini LLM
     |
     v
Grounded Answer + Sources
     |
     v
FastAPI
     |
     v
React + Vite
```

---

## Technology Stack

### Backend

- Python
- FastAPI
- FAISS
- Sentence Transformers
- LangChain
- Gemini
- PyPDF
- PyYAML

### Frontend

- React
- Vite
- JavaScript
- ESLint
- CSS

### Testing and Evaluation

- Pytest
- Retrieval Hit Rate
- Precision@K
- Recall@K
- Answer Generation Evaluation
- Faithfulness Evaluation

---

## Project Structure

```text
RAG-Production-Project/
|
|-- data/
|   `-- Rag_llm.pdf
|
|-- evaluation/
|   |-- __init__.py
|   |-- evaluate_answers.py
|   |-- evaluate_faithfulness.py
|   |-- evaluate_retrieval.py
|   `-- questions.json
|
|-- frontend/
|   |-- public/
|   |-- src/
|   |   |-- App.jsx
|   |   |-- App.css
|   |   |-- index.css
|   |   `-- main.jsx
|   |-- eslint.config.js
|   |-- index.html
|   |-- package.json
|   |-- package-lock.json
|   `-- vite.config.js
|
|-- src/
|   |-- api/
|   |   |-- main.py
|   |   `-- schemas.py
|   |
|   |-- chunking/
|   |   `-- chunker.py
|   |
|   |-- embeddings/
|   |   `-- embedder.py
|   |
|   |-- ingestion/
|   |   |-- index.py
|   |   `-- loader.py
|   |
|   |-- llm/
|   |   `-- llm_client.py
|   |
|   |-- prompts/
|   |   `-- prompt_templates.py
|   |
|   |-- retrieval/
|   |   `-- retriever.py
|   |
|   |-- utils/
|   |   |-- config.py
|   |   |-- exceptions.py
|   |   `-- logger.py
|   |
|   |-- vectordb/
|   |   `-- vector_store.py
|   |
|   `-- rag_pipeline.py
|
|-- tests/
|   |-- __init__.py
|   |-- test_api.py
|   |-- test_rag.py
|   `-- test_retriever.py
|
|-- .env
|-- .gitignore
|-- config.yaml
|-- main.py
|-- requirements.txt
`-- README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sidoji1/production-rag-system.git
cd production-rag-system
```

### 2. Create a Python Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

Do not commit the `.env` file to GitHub.

---

# Running the Application

The project uses two services:

```text
Backend  → FastAPI
Frontend → React + Vite
```

Both services should be running during development.

---

## Running the Backend

From the project root:

```powershell
uvicorn src.api.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Frontend

Open a second terminal.

Navigate to the frontend:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

## Using RAG Explorer

Open:

```text
http://localhost:5173
```

Enter a question such as:

```text
What are the main challenges of RAG?
```

The application will:

1. Send the question from React to FastAPI.
2. Validate the request.
3. Generate a query embedding.
4. Search the FAISS vector index.
5. Retrieve the most relevant document chunks.
6. Construct the RAG prompt.
7. Send the retrieved context to Gemini.
8. Generate a grounded answer.
9. Return the answer and source information.
10. Display the answer and retrieved sources in the React interface.

---

# API

## Health Check

```http
GET /health
```

Example:

```text
http://127.0.0.1:8000/health
```

---

## Query

```http
POST /query
```

Request:

```json
{
  "question": "What are the main challenges of RAG?"
}
```

Example response:

```json
{
  "question": "What are the main challenges of RAG?",
  "answer": "Based on the provided context...",
  "sources": [
    {
      "page": "1",
      "score": 0.7454
    }
  ]
}
```

---

# Testing

Run the complete test suite:

```powershell
pytest -v
```

Current test suite:

```text
9 passed
```

The tests cover:

- API health check
- Empty question validation
- Missing question validation
- Successful API query
- Successful RAG pipeline execution
- Empty RAG question handling
- Retriever Top-K behavior
- Empty retriever query handling
- Retriever failure handling

---

# Retrieval Evaluation

Run:

```powershell
python -m evaluation.evaluate_retrieval
```

The retrieval evaluation tests multiple Top-K configurations and reports:

- Retrieval Hit Rate
- Precision@K
- Recall@K

Current evaluation results:

```text
Retrieval Hit Rate: 100.00%
Average Recall@4: 100.00%
```

Top-K configurations tested:

```text
Top-K = 3
Top-K = 4
Top-K = 5
```

---

# Answer Evaluation

Run:

```powershell
python -m evaluation.evaluate_answers
```

The evaluation checks whether the RAG pipeline successfully generates answers for the evaluation questions.

Current result:

```text
Answer Generation Rate: 100.00%
Questions Evaluated: 5
```

---

# Example Questions

Try asking:

```text
What is Retrieval-Augmented Generation?
```

```text
What are the main challenges of RAG?
```

```text
What are the different paradigms of RAG?
```

```text
What are the main components of a RAG framework?
```

```text
What are the challenges faced by Naive RAG?
```

---

# Retrieval Results

The frontend displays the retrieved context used by the RAG pipeline.

For each retrieved source, the interface displays:

- Retrieval rank
- Page number
- Similarity score

Example:

```text
01    PAGE 1     74.5%
02    PAGE 2     71.4%
03    PAGE 14    70.2%
04    PAGE 3     69.1%
```

This provides visibility into which document chunks were retrieved before answer generation.

---

# Error Handling

The system includes custom exception handling for:

- Invalid questions
- Empty queries
- Retrieval failures
- RAG pipeline failures
- LLM generation failures
- Invalid API requests

The application also uses structured logging for easier debugging and monitoring.

---

# Configuration

Project configuration is maintained through:

```text
config.yaml
```

Environment secrets such as the Gemini API key are stored separately in:

```text
.env
```

The `.env` file is excluded from Git version control through `.gitignore`.

---

# Frontend

The frontend is built using React and Vite.

The interface provides:

- RAG Explorer branding
- Minimal visual design
- Question input
- Suggested questions
- Loading states
- Grounded answer display
- Source context display
- Retrieval similarity scores
- Error messages
- Responsive layout
- Ask another question functionality

The frontend communicates with the FastAPI backend through:

```text
POST http://127.0.0.1:8000/query
```

CORS is configured in the FastAPI application to allow local development from:

```text
http://localhost:5173
```

and:

```text
http://127.0.0.1:5173
```

---

# Development

## Backend

```text
Python
FastAPI
FAISS
Sentence Transformers
Gemini
LangChain
```

Run:

```powershell
uvicorn src.api.main:app --reload
```

## Frontend

```text
React
Vite
JavaScript
CSS
ESLint
```

Run:

```powershell
cd frontend
npm run dev
```

## Run Both Services

### Terminal 1

From the project root:

```powershell
.venv\Scripts\Activate.ps1
uvicorn src.api.main:app --reload
```

### Terminal 2

From the project root:

```powershell
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

# Evaluation Summary

The current project has been tested at multiple levels.

### Retrieval

```text
Hit Rate: 100.00%
Recall@4: 100.00%
```

### Answer Generation

```text
Answer Generation Rate: 100.00%
Questions Evaluated:    5
```

### Automated Tests

```text
9 passed
```

These evaluations provide separate checks for retrieval quality, answer generation, and application behavior.

---

# Project Status

The project currently includes:

- Production-oriented RAG backend
- PDF knowledge base
- Document loading
- Text chunking
- Sentence Transformer embeddings
- FAISS vector search
- Top-K retrieval
- Gemini answer generation
- Grounded responses
- Source attribution
- Similarity scores
- FastAPI REST API
- React + Vite frontend
- CORS configuration
- Error handling
- Structured logging
- Automated tests
- Retrieval evaluation
- Answer evaluation
- Git version control

---

# Future Improvements

Potential future improvements include:

- Streaming LLM responses
- Retrieval re-ranking
- Hybrid keyword + semantic retrieval
- Conversation history
- Multiple document support
- Document upload through the UI
- Advanced faithfulness scoring
- Response latency monitoring
- Authentication
- Production deployment
- Cloud hosting
- Persistent vector database management

---

# License

This project is intended for educational, portfolio, and demonstration purposes.

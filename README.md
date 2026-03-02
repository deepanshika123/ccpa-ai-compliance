# CCPA AI Compliance 

A FastAPI-based backend system that analyzes user prompts against legal statutes and identifies potentially harmful or non-compliant actions using a Retrieval-Augmented Generation (RAG) pipeline.

---

## Project Overview

This system processes legal statute documents, extracts sections, classifies them, and retrieves relevant legal references for a given user query.

The backend is designed to integrate with an LLM for intelligent legal reasoning.

---

##  Architecture

User Prompt
↓
Section Retrieval Engine
↓
RAG Pipeline
↓
LLM Analysis 
↓
Structured JSON Response

---

##  Features

- ✅ Statute PDF parsing
- ✅ Section extraction & classification
- ✅ Retrieval-based legal matching
- ✅ FastAPI clean architecture
- ✅ JSON-only API responses
- ✅ Input validation & error handling
- ✅ Stress tested backend
- ✅ Docker container support

---

## 🛠 Tech Stack

- Python 3.11
- FastAPI
- Pydantic
- PDFPlumber
- JSON-based Retrieval
- Docker

---

##  Project Structure

```
OpenHack/
│
├── app/
│ ├── main.py
│ ├── statute_parser.py
│ ├── classifier.py
│ ├── search_engine.py
│ └── rag_pipeline.py
│
├── data/
├── classified_sections.json
├── sections_output.json
├── test_parser.py
├── validate_format.py
├── stress_test.py
├── requirements.txt
└── README.md

```
---

## ⚙️ Local Setup

### 1. Clone Repository

git clone <repo-link>
cd OpenHack

### 2. Create Virtual Environment
python -m venv venv

Activate:
Windows
venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Run Server
uvicorn app.main:app --reload

Open API Docs:

http://127.0.0.1:8000/docs

---

## Testing

### 1. Format Validation
python validate_format.py
### 2. Stress Testing
python stress_test.py

## Docker Setup

### 1. Build Image
docker build -t legal-ai-backend .
### 2. Run Container
docker run -p 8000:8000 legal-ai-backend

Access API:
http://localhost:8000/docs


## API Endpoint
### 1. POST /analyze
######Request
{
  "prompt": "We sell customer data without consent"
}


######Response
{
  "harmful": true,
  "articles": [
    "Section 1798.120"
    ]
}

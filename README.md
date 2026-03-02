# CCPA-Guard: Enterprise-Grade Privacy Compliance Orchestrator

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Architecture](https://img.shields.io/badge/architecture-RAG_Microservice-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Abstract
CCPA-Guard is an advanced, fully containerized AI middleware designed to automate and enforce California Consumer Privacy Act (CCPA) compliance checks. Utilizing a Retrieval-Augmented Generation (RAG) architecture, the platform seamlessly bridges the gap between complex legal frameworks and operational business practices. It operates with zero human-in-the-loop dependencies, delivering deterministic, structured JSON evaluations with sub-second retrieval latency.

## Core Architecture & Modules

The system is structurally divided into three primary pipelines, governed by a strict formatting and safety middleware.



### 1. Semantic Search & Retrieval Engine (Data Layer)
This module acts as the deterministic foundation of the system, ensuring the AI only reasons over verified legal texts.
* **Vectorized Knowledge Base:** The CCPA legal framework is pre-processed and converted into high-dimensional embeddings.
* **Low-Latency Similarity Search:** Utilizes `all-MiniLM-L6-v2` (Sentence Transformers) to perform cosine-similarity searches, extracting the top-K most relevant legal sections based on the incoming business practice query.

### 2. Contextual AI Evaluation Engine (Logic Layer)
A high-performance computational environment for legal reasoning, isolated within a secure Docker container.
* **Quantized Large Language Model:** Powered by `Mistral-7B-Instruct-v0.2`.
* **Memory Optimization:** Implements 4-bit precision loading (`BitsAndBytesConfig`) with double quantization and FP16 compute datatypes, allowing enterprise-grade LLMs to operate efficiently on constrained edge nodes or cloud instances.
* **Zero-Shot Legal Reasoning:** Analyzes the retrieved semantic context against the user query using strict prompt engineering to prevent LLM hallucination.

### 3. Safety Net & Telemetry Middleware
Ensures all outputs strictly adhere to downstream integration requirements.
* **Regex-Driven JSON Parsing:** Automatically isolates and extracts valid JSON payloads from raw LLM generated text.
* **Stateful Fallback Logic:** Intercepts and overrides ambiguous model outputs, forcibly clearing the cited articles array if the evaluated practice is deemed non-harmful (Safe).

## Technical Specifications & Stack

* **Core Orchestrator (Backend):** Python 3.10 running on the FastAPI framework. Handles route multiplexing and asynchronous request processing.
* **Artificial Intelligence Engine:** `transformers`, `torch`, and `accelerate` ecosystems.
* **Embedding Model:** `sentence-transformers` for robust text vectorization.
* **Deployment & Containerization:** Docker (Isolated Linux Environment). Implements aggressive layer caching and build-time model downloading to ensure `<5 minute` cold-start times.

## Deployment & Initialization

To initialize the assessment engine via Docker, ensure the Docker Daemon is running and you possess a valid Hugging Face access token for the gated Mistral model.

### 1. Build the Microservice Image
The build process automatically pulls and bakes the LLM weights into the image to prevent runtime latency.
```bash
docker build --build-arg HF_TOKEN="your_huggingface_token" -t cortex-ccpa .
```

### 2. Initialize the Container
```bash
docker run -p 8000:8000 -e HF_TOKEN="your_huggingface_token" cortex-ccpa
```

### 3. Interacting with the Assessment Interface
Send a POST request to the inference endpoint.

```bash
curl -X POST [http://127.0.0.1:8000/analyze](http://127.0.0.1:8000/analyze) \
-H "Content-Type: application/json" \
-d '{"prompt": "We sell customer browsing history to ad networks without providing an opt-out link on our homepage."}'
```

**Expected JSON Response:**
```json
{
  "harmful": true,
  "articles": [
    "Section 1798.135"
  ]
}
```


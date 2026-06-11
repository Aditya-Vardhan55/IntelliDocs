# 🧠 IntelliDocs - Universal Document Intelligence Platform

> Production-grade Universal Document Intelligence Platform supporting Legal, Medical, Corporate and Code domains with RAG pipeline, LangSmith observability, MLflow experiment tracking, Redis caching reducing API costs by 40%, fully containerized with Docker and deployed via GitHub Actions CI/CD.

> Production-grade RAG platform supporting Legal, Medical, Corporate,
> and Code documents with full MLOps/LLMOps observability stack.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![LangChain](https://img.shields.io/badge/LangChain-latest-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-manifests-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-black)

---

## What Is This

IntelliDocs is a document Q&A platform that lets users upload any document and ask natural language questions about it.
The system auto-detects the document domain and applies domain-specific retrieval and prompting strategies.

**Supported domains:**
- ⚖️ Legal - contracts, NDAs, agreements
- 🏥 Medical - research papers, clinical documents
- 🏢 Corporate - HR policies, internal wikis
- 💻 Code - repositories, technical documentation 

---

## Architecture

User (Streamlit UI)
↓
FastAPI Backend (async REST API)
↓
LangChain RAG Pipeline
├── Domain Router (keyword detection)
├── Domain-specific chunking strategy
├── HuggingFace Embeddings (all-MiniLM-L6-v2)
└── ChromaDB Vector Store
↓
Ollama + llama3.2 (local LLM, zero API cost)
↓
─────────────────────────────
LLMOps Layer (LangSmith)
├── Full prompt/response tracing
├── Latency per LLM call
└── Token usage tracking
─────────────────────────────
MLOps Layer (MLflow)
├── Chunking strategy experiments
├── Document processing metrics
└── Query performance tracking
─────────────────────────────
Caching Layer (Redis)
├── MD5 hash-based cache keys
├── 1-hour TTL
└── ~40% repeated query reduction
─────────────────────────────
Deployment Layer
├── Docker Compose (local)
├── GitHub Actions CI/CD
└── Kubernetes manifests (cloud-ready)

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | FastAPI | Async, high performance, auto Swagger docs |
| RAG | LangChain | Pipeline abstractions, prompt management |
| Vector Store | ChromaDB | Local, persistent, no external service needed |
| Embeddings | all-MiniLM-L6-v2 | Free, CPU-friendly, 384 dimensions |
| LLM | Ollama + llama3.2 | Zero API cost, data stays local |
| LLMOps | LangSmith | Full LLM call observability |
| MLOps | MLflow | Experiment tracking, chunking strategy comparison |
| Caching | Redis | Repeated query optimization |
| Frontend | Streamlit | Rapid UI, cache hit visualization |
| CI/CD | GitHub Actions | Automated test + Docker build pipeline |
| Containers | Docker Compose | Single command local deployment |
| Orchestration | Kubernetes | Production-ready manifests for AWS EKS/GKE |

---

## Key Design Decisions

**Why domain-specific chunking?**
Legal documents need large chunks (1000 tokens) -
clauses span paragraphs and splitting mid-clause
destroys meaning. Code needs small chunks (400 tokens)
- functions are self-contained. This was measured
and tracked in MLflow.

**Why Ollama over OpenAI?**
Legal and medical documents cannot leave the machine.
Ollama runs entirely locally - zero data privacy risk,
zero API cost. Model is swappable via one env var change.

**Why ChromaDB over Pinecone?**
No external service, no API keys, runs in Docker,
persists to disk. For a self-hosted platform this
is right tradeoff.

**Why Redis caching?**
HR policy documents get the same questions repeatedly.
Caching eliminates redundant LLM calls. Cache hit
rate tracked in health endpoint.

---

## Running Locally

### Prerequisites
- Docker Desktop
- Ollama installed (`ollama pull llama3.2`)
- LangSmith API key (free at smith.langchain.com)

### One command startup
```bash
git clone https://github.com/yourusername/intellidocs
cd intellidocs/docker
docker-compose up --build
```

### Access points
| Service | URL |
|---------|-----|
| Streamlit UI | http://localhost:8501 |
| FastAPI Swagger | http://localhost:8000/docs |
| MLflow Dashboard | http://localhost:5000 |
| Prometheus Metrics | http://localhost:8000/metrics |

---

## CI/CD Pipeline

Push to main
↓
CI — GitHub Actions
├── Fresh Ubuntu environment
├── Install dependencies
└── Run test suite (domain router, API, cache)
↓ (only on CI pass)
CD — GitHub Actions
├── Build Docker images
├── Push to Docker Hub
└── Tag with :latest + commit SHA

---

## Kubernetes Deployment

Production-ready manifests in `/k8s`:

```bash
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/secrets.yml
kubectl apply -f k8s/redis-deployment.yml
kubectl apply -f k8s/mlflow-deployment.yml
kubectl apply -f k8s/ollama-deployment.yml
kubectl apply -f k8s/backend-deployment.yml
kubectl apply -f k8s/frontend-deployment.yml
```

> Designed for AWS EKS or GCP GKE where nodes 
> have sufficient RAM for the full Ollama model.

---

## Project Structure

intellidocs/
├── backend/
│   ├── main.py              # FastAPI entrypoint
│   ├── routers/             # upload, query, health
│   ├── services/            # RAG pipeline, embeddings,
│   │                        # domain router, cache
│   ├── prompts/             # 4 domain-specific templates
│   └── config.py            # Pydantic settings
├── frontend/
│   └── app.py               # Streamlit UI
├── vectorstore/
│   └── chroma_client.py     # ChromaDB setup
├── mlops/
│   └── mlflow_tracker.py    # Experiment tracking
├── llmops/
│   └── langsmith_config.py  # LLM tracing
├── k8s/                     # Kubernetes manifests
├── docker/                  # Dockerfiles + Compose
├── .github/workflows/       # CI/CD pipelines
└── tests/                   # pytest suite

---

## Author

**Aditya Vardhan**
[LinkedIn](https://www.linkedin.com/in/aditya-vardhan07/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
Version - Mk I
---
title: RAG Medical Chatbot
emoji: 🏥
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 5000
---

# 🏥 RAG Medical Chatbot — LLMOps End-to-End Project

A production-ready Medical Question Answering chatbot built using Retrieval-Augmented Generation (RAG), deployed with a complete MLOps pipeline including CI/CD, containerization, security scanning, and cloud deployment.

🚀 **Live Demo:** [https://huggingface.co/spaces/zainsardar/rag-medical-chatbot](https://huggingface.co/spaces/zainsardar/rag-medical-chatbot)

---

## 📌 Project Overview

This project demonstrates an end-to-end LLMOps workflow where medical PDF documents are loaded, chunked, embedded into a FAISS vector store, and retrieved at query time to generate accurate answers using a Large Language Model (LLaMA3 via Groq API).

---

## 🏗️ Architecture

```
User Query
    ↓
Flask Web App (Frontend + Backend)
    ↓
Retriever (LangChain LCEL Chain)
    ↓
FAISS Vector Store ←── Medical PDFs (chunked + embedded)
    ↓
Groq API (LLaMA3 8B)
    ↓
Answer returned to User
```

### CI/CD Pipeline
```
GitHub Push
    ↓
Jenkins Pipeline
    ↓
Docker Build
    ↓
Aqua Trivy Security Scan
    ↓
Push to AWS ECR
    ↓
Deploy to AWS App Runner
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| **Embedding Model** | `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace) |
| **Vector Store** | FAISS (Meta) — local CPU |
| **RAG Framework** | LangChain 1.x (LCEL style) |
| **LLM Provider** | Groq API + LLaMA3 (`llama-3.1-8b-instant`) |
| **PDF Loader** | PyPDF + LangChain DirectoryLoader |
| **Backend** | Flask 3.x |
| **Frontend** | HTML / CSS / JavaScript |
| **Containerization** | Docker |
| **Security Scanning** | Aqua Trivy |
| **CI/CD** | Jenkins |
| **Container Registry** | AWS ECR |
| **Cloud Deployment** | AWS App Runner + HuggingFace Spaces |
| **Source Control** | GitHub |

---

## 📁 Project Structure

```
RAG MEDICAL CHATBOT/
├── app/
│   ├── common/
│   │   ├── logger.py              # Custom logger
│   │   └── custom_exception.py    # Custom exception handler
│   ├── components/
│   │   ├── pdf_loader.py          # PDF loading + text chunking
│   │   ├── embeddings.py          # HuggingFace embeddings
│   │   ├── vector_store.py        # FAISS vector store
│   │   ├── retriever.py           # LangChain LCEL QA chain
│   │   ├── llm.py                 # Groq LLM setup
│   │   └── data_loader.py         # Combines loader, embeddings & vector store
│   ├── config/
│   │   └── config.py              # All configuration variables
│   ├── templates/
│   │   └── index.html             # Frontend UI
│   └── application.py             # Flask app entry point
├── custom_jenkins/
│   └── Dockerfile                 # Custom Jenkins with Docker installed
├── data/                          # Medical PDF files
├── vectorstore/                   # FAISS index files
├── logs/                          # Application logs
├── .env                           # API keys (never commit!)
├── .dockerignore                  # Docker build exclusions
├── .gitattributes                 # Git LFS tracking config
├── .gitignore                     # Git exclusions
├── Dockerfile                     # App Docker image
├── Jenkinsfile                    # CI/CD pipeline definition
├── requirements.txt               # Local development dependencies
├── requirements-docker.txt        # Docker deployment dependencies (CPU torch)
└── setup.py                       # Package setup
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```env
HF_TOKEN=your_huggingface_token_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_flask_secret_key_here
```

Get your API keys:
- **HuggingFace Token** → https://huggingface.co/settings/tokens
- **Groq API Key** → https://console.groq.com

### Config Variables (`app/config/config.py`)

| Variable | Value | Description |
|---|---|---|
| `GROQ_API_KEY` | from `.env` | Groq API key |
| `HF_TOKEN` | from `.env` | HuggingFace token |
| `DB_FAISS_PATH` | `vectorstore/db_faiss` | FAISS index path |
| `DATA_PATH` | `data/` | PDF files directory |
| `CHUNK_SIZE` | `500` | Text chunk size |
| `CHUNK_OVERLAP` | `50` | Chunk overlap size |

---

## 🚀 Local Installation & Setup

### Step 1 — Clone the repository
```bash
git clone https://github.com/zainsardar0/RAG-MEDICAL-CHATBOT.git
cd RAG-MEDICAL-CHATBOT
```

### Step 2 — Create virtual environment
```bash
python -m venv venv
```

### Step 3 — Activate virtual environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 4 — Install dependencies
```bash
pip install -r requirements.txt
pip install -e .
```

### Step 5 — Set up environment variables
Create a `.env` file in the root directory:
```env
HF_TOKEN=your_huggingface_token_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_flask_secret_key
```

### Step 6 — Run the application
```bash
python app/application.py
```

The app will automatically:
1. Check if vectorstore exists
2. If not — load PDFs, create embeddings, save FAISS index
3. Start Flask server at `http://localhost:5000`

---

## 🐳 Docker Setup

### Build the Docker image locally
```bash
docker build -t rag-medical-chatbot:latest .
```

### Run the container
```bash
docker run -p 5000:5000 \
  -e GROQ_API_KEY=your_key \
  -e HF_TOKEN=your_token \
  rag-medical-chatbot:latest
```

### Note on Docker requirements
The project uses two separate requirements files:

| File | Used For | Torch Version |
|---|---|---|
| `requirements.txt` | Local development | Full torch (from venv) |
| `requirements-docker.txt` | Docker deployment | `torch==2.5.1+cpu` (lighter) |

This reduces Docker image size significantly by using CPU-only PyTorch.

---

## 🤗 HuggingFace Spaces Deployment

The app is deployed on HuggingFace Spaces using Docker SDK.

### Steps to deploy on HuggingFace Spaces:

**Step 1 — Create a new Space:**
- Go to https://huggingface.co/spaces
- Click `New Space`
- SDK: `Docker`
- Visibility: `Public`

**Step 2 — Install Git LFS:**
```bash
git lfs install
git lfs track "*.pdf"
git lfs track "*.faiss"
git lfs track "*.pkl"
git add .gitattributes
git commit -m "feat: add git lfs tracking"
```

**Step 3 — Add HF Space as remote and push:**
```bash
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
git push space main --force
```

**Step 4 — Add Secrets in Space Settings:**

| Secret Name | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |
| `HF_TOKEN` | Your HuggingFace token |
| `HUGGINGFACEHUB_API_TOKEN` | Your HuggingFace token |
| `SECRET_KEY` | Flask session secret key |

---

## 🔧 Jenkins CI/CD Pipeline

### Jenkins Setup (Custom Docker Image)

```bash
# Build custom Jenkins image
cd custom_jenkins
docker build -t jenkins-dind:latest .

# Run Jenkins container
docker run -d \
  --name jenkins-dind \
  --privileged \
  -p 8080:8080 \
  -p 50000:50000 \
  jenkins-dind:latest
```

### After every Jenkins restart
```bash
docker exec -u root -it jenkins-dind chmod 666 /var/run/docker.sock
```

### Pipeline Stages

```
Stage 1: Clone GitHub Repo
    ↓
Stage 2: Build Docker Image
    ↓
Stage 3: Trivy Security Scan
    ↓
Stage 4: Push to AWS ECR
    ↓
Stage 5: Deploy to AWS App Runner (optional)
```

### Jenkins Credentials Required

| Credential ID | Type | Purpose |
|---|---|---|
| `github-token` | Secret text | GitHub personal access token |
| `aws-token` | AWS credentials | AWS access key + secret key |

### WSL2 Memory Configuration (Windows)

To prevent Docker Desktop crashes during large builds, create `C:\Users\USERNAME\.wslconfig`:

```ini
[wsl2]
memory=6GB
processors=4
swap=2GB
```

Then run:
```bash
wsl --shutdown
```

---

## 🔍 How RAG Works in This Project

```
1. PDF Loading
   └── DirectoryLoader loads all PDFs from data/ folder

2. Text Chunking
   └── RecursiveCharacterTextSplitter
       ├── chunk_size = 500
       └── chunk_overlap = 50

3. Embeddings
   └── HuggingFaceEmbeddings
       └── model: sentence-transformers/all-MiniLM-L6-v2

4. Vector Store
   └── FAISS (stored locally at vectorstore/db_faiss)

5. Retrieval (LCEL Chain)
   └── User query → FAISS similarity search → Top K chunks

6. Answer Generation
   └── LLaMA3 (via Groq) + retrieved context → Final answer
```

---

## 🔄 LangChain LCEL Chain

This project uses the modern LangChain LCEL style instead of the deprecated `RetrievalQA`:

```python
qa_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Usage - returns plain string
result = qa_chain.invoke(user_question)
```

---

## 📦 Key Package Versions

| Package | Version |
|---|---|
| `langchain` | 1.2.10 |
| `langchain_community` | 0.4.1 |
| `langchain_huggingface` | 1.2.1 |
| `langchain_groq` | 1.1.2 |
| `faiss-cpu` | 1.13.2 |
| `flask` | 3.1.3 |
| `sentence-transformers` | 5.2.3 |
| `torch` | 2.10.0 (local) / 2.5.1+cpu (Docker) |

---

## 👤 Author

**Muhammad Zain Ul Abideen**
- GitHub: [@zainsardar0](https://github.com/zainsardar0)
- HuggingFace: [@zainsardar](https://huggingface.co/zainsardar)

---

## 📄 License

This project is open source and available under the MIT License.

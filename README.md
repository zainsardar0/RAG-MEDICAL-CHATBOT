---
title: RAG Medical Chatbot
emoji: 🏥
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 5000
---

# 🏥 RAG Medical Chatbot

An AI-powered medical question-answering chatbot built with Retrieval-Augmented Generation (RAG). The application loads medical PDF documents, converts them into searchable vector embeddings, retrieves relevant context for a user question, and generates a concise answer using an LLM.

🚀 **Live Demo:** [https://huggingface.co/spaces/zainsardar/rag-medical-chatbot](https://huggingface.co/spaces/zainsardar/rag-medical-chatbot)

---

## 📌 Project Overview

RAG Medical Chatbot is a document-based medical assistant that answers questions from the medical PDFs available in the project. Instead of relying only on the LLM's general knowledge, the system first searches the medical document collection and then uses the retrieved context to generate a response.

The goal of this project is to demonstrate a practical RAG pipeline using LangChain, FAISS, HuggingFace embeddings, Groq LLMs, Flask, and Docker.

> ⚠️ **Medical Disclaimer:** This project is for educational and portfolio purposes only. It is not a replacement for professional medical advice, diagnosis, or treatment.

---

## ✨ Features

- Medical PDF document loading
- Text chunking for long documents
- HuggingFace embedding generation
- FAISS-based semantic search
- LangChain LCEL-based RAG chain
- Groq LLaMA3 model integration
- Flask web interface
- Chat-style user interface
- Custom logging and exception handling
- Environment-based configuration
- Dockerized application setup

---

## 🏗️ System Architecture

```
Medical PDFs
    ↓
PDF Loader
    ↓
Text Chunking
    ↓
HuggingFace Embeddings
    ↓
FAISS Vector Store
    ↓
User Question → Retriever → Relevant Context
    ↓
Prompt + Groq LLaMA3
    ↓
Generated Answer
    ↓
Flask Web Interface
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | FAISS |
| RAG Framework | LangChain LCEL |
| LLM Provider | Groq API + LLaMA3 |
| PDF Processing | PyPDF + LangChain DirectoryLoader |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Containerization | Docker |
| Configuration | Python Dotenv |
| Source Control | GitHub |

---

## 📁 Project Structure

```
RAG-MEDICAL-CHATBOT/
├── app/
│   ├── common/
│   │   ├── logger.py              # Custom logger
│   │   └── custom_exception.py    # Custom exception handler
│   ├── components/
│   │   ├── pdf_loader.py          # PDF loading and text chunking
│   │   ├── embeddings.py          # HuggingFace embedding model
│   │   ├── vector_store.py        # FAISS vector store save/load logic
│   │   ├── retriever.py           # LangChain LCEL RAG chain
│   │   ├── llm.py                 # Groq LLM setup
│   │   └── data_loader.py         # Data ingestion helper
│   ├── config/
│   │   └── config.py              # Project configuration
│   ├── templates/
│   │   └── index.html             # Web UI template
│   └── application.py             # Flask app entry point
├── data/                          # Medical PDF files
├── vectorstore/                   # Local FAISS index files
├── logs/                          # Application logs
├── .env                           # Local environment variables, not committed
├── .dockerignore                  # Docker exclusions
├── .gitignore                     # Git exclusions
├── Dockerfile                     # Docker image definition
├── requirements.txt               # Local dependencies
├── requirements-docker.txt        # Docker dependencies
└── setup.py                       # Package setup
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
HF_TOKEN=your_huggingface_token_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_flask_secret_key_here
```

Optional configuration values:

```env
DATA_PATH=data/
DB_FAISS_PATH=vectorstore/db_faiss
CHUNK_SIZE=500
CHUNK_OVERLAP=50
RETRIEVER_K=3
```

---

## 🚀 Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/zainsardar0/RAG-MEDICAL-CHATBOT.git
cd RAG-MEDICAL-CHATBOT
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Add environment variables

Create a `.env` file and add your API keys.

### 5. Run the app

```bash
python app/application.py
```

Open the app at:

```text
http://localhost:5000
```

When the app starts, it checks whether the FAISS vector store already exists. If it does not exist, the app loads PDFs from the `data/` folder, creates chunks, generates embeddings, and saves the FAISS index locally.

---

## 🐳 Docker Setup

### Build the Docker image

```bash
docker build -t rag-medical-chatbot:latest .
```

### Run the Docker container

```bash
docker run -p 5000:5000 \
  -e GROQ_API_KEY=your_groq_api_key \
  -e HF_TOKEN=your_huggingface_token \
  -e HUGGINGFACEHUB_API_TOKEN=your_huggingface_token \
  -e SECRET_KEY=your_flask_secret_key \
  rag-medical-chatbot:latest
```

Then open:

```text
http://localhost:5000
```

---

## 🔍 How RAG Works in This Project

1. **PDF Loading**  
   Medical PDFs are loaded from the `data/` directory.

2. **Text Chunking**  
   Long PDF text is split into smaller chunks so that relevant sections can be retrieved later.

3. **Embedding Generation**  
   Each chunk is converted into a numerical vector using a HuggingFace sentence-transformer model.

4. **Vector Storage**  
   The vectors are stored in a local FAISS vector database.

5. **Semantic Retrieval**  
   When the user asks a question, FAISS retrieves the most relevant chunks.

6. **Answer Generation**  
   The retrieved context and user question are passed to a Groq-hosted LLaMA3 model to generate the final answer.

---

## 🔄 LangChain LCEL Chain

The project uses LangChain LCEL to connect the retriever, prompt, LLM, and output parser:

```python
qa_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

---

## 🧠 What I Learned

Through this project, I practiced:

- Building a document-based RAG system
- Loading and processing PDF documents
- Creating embeddings using sentence-transformer models
- Storing and searching vectors with FAISS
- Designing prompts for safer medical question answering
- Connecting an LLM API with a retrieval pipeline
- Building a Flask-based AI web application
- Containerizing an AI application with Docker

---

## 🚧 Future Improvements

- Add source citations with PDF name and page number
- Add user PDF upload support
- Add chat history memory
- Add response streaming
- Add similarity score display for retrieved chunks
- Add basic test cases
- Add a FastAPI version of the backend
- Improve UI design

---

## 👤 Author

**Muhammad Zain Ul Abideen**

- GitHub: [@zainsardar0](https://github.com/zainsardar0)
- HuggingFace: [@zainsardar](https://huggingface.co/zainsardar)

---

## 📄 License

This project is open source and available under the MIT License.

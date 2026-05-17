import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.environ.get("HF_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
DB_FAISS_PATH = os.environ.get("DB_FAISS_PATH", "vectorstore/db_faiss")
DATA_PATH = os.environ.get("DATA_PATH", "data/")
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", 50))
RETRIEVER_K = int(os.environ.get("RETRIEVER_K", 3))

import os
from dotenv import load_dotenv

load_dotenv()

# Appelle d'Ollama
OLLAMA_HOST=os.getenv("OLLAMA_HOST","http://localhost:11434")
OLLAMA_CHAT_MODEL=os.getenv("OLLAMA_CHAT_MODEL","llama3.1:8b")
OLLAMA_EMBED_MODEL=os.getenv("OLLAMA_EMBED_MODEL","qwen3-embedding:0.6b")

# Scraping
SITE_BASE_URL=os.getenv("SITE_BASE_URL","https://www.jokerscompany.com")

# Decoupages
CHUNK_SIZE=int(os.getenv("CHUNK_SIZE",500))
CHUNK_OVERLAP=int(os.getenv("CHUNK_OVERLAP",50))

# ChromaDB
CHROMA_PERSIST_DIR=os.getenv("CHROMA_PERSIST_DIR","data/vectorstore/chroma")
CHROMA_COLLECTION_NAME=os.getenv("CHROMA_COLLECTION_NAME","jokerscompany_infos")

# RAG
TOP_K=int(os.getenv("TOP_K",5))

# Chemins des données
RAW_DATA_DIR="data/raw/website"
CHUNKS_FILE="data/processed/chunks.json"
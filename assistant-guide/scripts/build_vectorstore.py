import json
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.vectorstore import add_chunks_to_store
from src.utils.logger import get_logger

logger=get_logger(__name__)

EMBEDDING_FILE="data/processed/chunks_with_embeddings.json"

def main():
    with open(EMBEDDING_FILE, "r", encoding="utf-8") as f:
        embedded_chunks=json.load(f)
    
    add_chunks_to_store(embedded_chunks)
    
if __name__=="__main__":
    main()
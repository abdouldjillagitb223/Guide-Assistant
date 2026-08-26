import json
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.embeddings import embed_chunks
from src.config import CHUNKS_FILE
from src.utils.logger import get_logger

logger=get_logger(__name__)

EMBEDDED_FILE="data/processed/chunks_with_embeddings.json"

def main():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks=json.load(f)
        
    logger.info(f"{len(chunks)} chunks à vectoriser...")
    embedded_chunks=embed_chunks(chunks)
    
    with open(EMBEDDED_FILE, "w", encoding="utf-8") as f:
        json.dump(embedded_chunks, f, ensure_ascii=False, indent=2)
        
    logger.info(f"Terminé. Embeddings écrits dans {EMBEDDED_FILE}")

if __name__=="__main__":
    main()
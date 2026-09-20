import argparse
import json
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.vectorstore import add_chunks_to_store, reset_collection
from src.utils.logger import get_logger

logger=get_logger(__name__)

EMBEDDING_FILE="data/processed/chunks_with_embeddings.json"

def main():
    parser=argparse.ArgumentParser(
        description="Construit (ou reconstruit) le vectorstore Chromadb à partir des chunks vectorisée."
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Supprime entièrement la collection existante avant de la repeupler"
            "(remplacement complet, au lieu d'un upsert incrémental)."
    )
    args=parser.parse_args()
    
    with open(EMBEDDING_FILE, "r", encoding="utf-8") as f:
        embedded_chunks=json.load(f)
    
    if args.reset:
        logger.info("Remplacement complet demandé: la collection existante va être vidée.")
        reset_collection()
        
    add_chunks_to_store(embedded_chunks)
    
if __name__=="__main__":
    main()
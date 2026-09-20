import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion.chunker import chunk_page
from src.ingestion.metadata import build_metadata
from src.config import RAW_DATA_DIR, CHUNKS_FILE
from src.utils.logger import get_logger

logger=get_logger(__name__)

def main():
    os.makedirs(os.path.dirname(CHUNKS_FILE), exist_ok=True)
    
    all_chunks_with_metadata=[]
    
    raw_files=[f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".json")]
    logger.info(f"{len(raw_files)} fichier(s) trouvé (s) dans {RAW_DATA_DIR}")

    for filename in raw_files:
        filepath=os.path.join(RAW_DATA_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            page=json.load(f)
        
        blocks=page.get("blocks", [])
        if not blocks:
            logger.warning(f"Aucun bloc structuré trouvé dans {filename}, page ignorée.")
            continue
        
        chunks=chunk_page(blocks)
        logger.info(f"{filename}-> {len(chunks)} chunk(s) générés.")
        
        for i, chunk in enumerate(chunks):
            metadata=build_metadata(page, chunk, i, len(chunks)) 
            all_chunks_with_metadata.append({
                "text":chunk["text"],
                "metadata":metadata
            })
    
    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks_with_metadata, f, ensure_ascii=False, indent=2)
    logger.info(f"Terminé. {len(all_chunks_with_metadata)} chunks écrits dans {CHUNKS_FILE}")
    
if __name__=="__main__":
    main()
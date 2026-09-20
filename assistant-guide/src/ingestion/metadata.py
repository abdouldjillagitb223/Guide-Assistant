from urllib.parse import urlparse
import hashlib
from datetime import datetime, timezone

def generate_chunk_id(url:str, chunk_index:int):
    """Génère un identifiant stable et unique pour un chunk (utile pour ChromaDB)."""
    raw=f"{url}#{chunk_index}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def build_metadata(
    page:dict,
    chunk:dict,
    chunk_index:int,
    total_chunks:int
):
    """
    Construire les métadonnnées associées à un chunk, à partir des informations
    de la page d'origine (url, title) et chunk lui-même par (heading de section).
    """
    return {
        "chunk_id":generate_chunk_id(page["url"], chunk_index),
        "url":page["url"],
        "title":page.get("title",""),
        "section_heading":chunk["heading"],
        "chunk_index":chunk_index,
        "total_chunks":total_chunks,
        "source":urlparse(page["url"]).netloc,
        "language":"fr",
        "ingested_at":datetime.now(timezone.utc).isoformat(),
    }
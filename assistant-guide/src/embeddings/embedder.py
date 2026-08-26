import ollama
from src.config import OLLAMA_HOST, OLLAMA_EMBED_MODEL
from src.utils.logger import get_logger

logger=get_logger(__name__)

user=ollama.Client(host=OLLAMA_HOST)

def embed_text(text:str):
    """
    Transforme un text en vecteur numérique via le modèle d'embedding Ollama.
    """ 
    try:
        response=user.embeddings(model=OLLAMA_EMBED_MODEL, prompt=text)
        return response["embedding"]
    except Exception as e:
        logger.error(f"Échec de l'embedding:{e}")
        raise
    
def embed_chunks(chunks:list[dict]):
    """
    Ajoute un vecteur d'embedding à chaque chunk.
    chunks: liste de dicts {text, metadata} (le format produit par create_chunks.py).
    Retourne la même liste, enrichie d'une clé "embedding" par élément.
    """    
    embedded=[]
    total=len(chunks)

    for i, chunk in enumerate(chunks, start=1):
        vector=embed_text(chunk["text"])
        embedded.append({
            "text":chunk["text"],
            "metadata":chunk["metadata"],
            "embedding":vector
        })
        logger.info(f"Embedding {i}/{total}-{chunk['metadata']['section_heading']}")
        
    return embedded
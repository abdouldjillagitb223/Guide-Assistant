from src.vectorstore import search_similar_chunks
from src.config import TOP_K
from src.utils.logger import get_logger

logger=get_logger(__name__)

def retrieve_context(query:str, top_k:int=TOP_K):
    """ 
    Récupère les chunks les plus pertinents pour une question donnée.
    Retourne la liste brute des résultats (text, metadata, distance),
    triée par pertinence (déjà fait par ChromaDB).
    """
    results=search_similar_chunks(query, top_k=top_k)
    logger.info(f"{len(results)} chunk(s) récupéré(s) pour la question:{query!r}")
    return results

def format_context(chunks:list[dict]):
    """ 
    Assemble les chunks récupérés en un bloc de texte structuré,
    prêt à être injecté dans le prompt du modèle de génération.
    Chaque chunk est numéroté et associé à sa section source.
    """
    if not chunks:
        return "Aucune information pertinente trouvée."
    
    blocks=[]
    for i, chunk in enumerate(chunks, start=1):
        heading=chunk["metadata"].get("section_heading", "")
        blocks.append(f"[Source{i}-{heading}]\n{chunk['text']}")
    
    return "\n\n".join(blocks)
from src.vectorstore.chroma_store import get_or_create_collection
from src.embeddings.embedder import embed_text
from src.config import TOP_K

def search_similar_chunks(query:str,top_k:int=TOP_K):
    """ 
    Vectorise la question utilisateur et recherche les chunks les plus proches
    sémantiquement dans ChromaDB. Retourne une liste de dicts {text, metadata, distance}. 
    """
    collection=get_or_create_collection()
    query_embedding=embed_text(query)
    
    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    matches=[]
    for i in range(len(results["ids"][0])):
        matches.append({
            "text":results["documents"][0][i],
            "metadata":results["metadatas"][0][i],
            "distance":results["distances"][0][i]
        })
    
    return matches
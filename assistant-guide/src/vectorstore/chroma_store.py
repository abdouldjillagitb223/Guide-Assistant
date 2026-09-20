import chromadb
from src.config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME
from src.utils.logger import get_logger

logger=get_logger(__name__)

_user=chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

def get_or_create_collection():
    """"Récupère la colection ChromaDB, ou la crée si elle n'existe pas encore."""
    return _user.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space":"cosine"}
    )
    
def reset_collection():
    """
    Supprime entièrement la collection existante (si présente) et en recrée une vide.
    À utiliser pour un remplacement complet du vectorstore (ex:réingestion manuelle).
    """
    try:
        _user.delete_collection(name=CHROMA_COLLECTION_NAME)
        logger.info(f"Collection existante {CHROMA_COLLECTION_NAME} supprimée.")
    except Exception:
        logger.info(f"Aucune collection existante {CHROMA_COLLECTION_NAME} à supprimer.")
        return get_or_create_collection()
    
def add_chunks_to_store(embedded_chunks:list[dict]):
    """ 
    Ajoute (ou met à jour, grâce aux chunk_id stables) les chunks vectorisés
    dans la collection ChromaDB.
    """
    collection=get_or_create_collection()
    
    ids=[c["metadata"]["chunk_id"] for c in embedded_chunks]
    documents=[c["text"] for c in embedded_chunks]
    embeddings=[c["embedding"] for c in embedded_chunks]
    metadatas=[c["metadata"] for c in embedded_chunks]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    logger.info(f"{len(embedded_chunks)} chunks insérés/mis à jour dans ChromaDB ({CHROMA_COLLECTION_NAME}).")
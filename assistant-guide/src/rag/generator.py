import ollama
from src.config import OLLAMA_HOST, OLLAMA_CHAT_MODEL
from src.utils.logger import get_logger

logger=get_logger(__name__)

user=ollama.Client(host=OLLAMA_HOST)

def generate_answer(messages:list[dict]):
    """
    Envoie les messages (system + user) au modèle de génération Ollama 
    et retourne la réponse textuelle.
    """
    try:
        response=user.chat(
            model=OLLAMA_CHAT_MODEL,
            messages=messages,
            stream=False
        )
        
        return response["message"]["content"]
    except Exception as e:
        logger.error(f"Échec de la génération:{e}")
        raise
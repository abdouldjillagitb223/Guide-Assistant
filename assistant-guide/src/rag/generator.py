from src.config import GROQ_CHAT_MODEL, GROQ_API_KEY
from src.utils.logger import get_logger

from groq import Groq

logger=get_logger(__name__)

user=Groq(
    api_key=GROQ_API_KEY
)

def generate_answer(messages:list[dict]):
    """
    Envoie les messages (system + user) au modèle de génération Ollama 
    et retourne la réponse textuelle.
    """
    try:
        response=user.chat.completions.create(
            model=GROQ_CHAT_MODEL,
            messages=messages,
            stream=False
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Échec de la génération:{e}")
        raise

def generate_answer_stream(messages:list[dict]):
    """ 
    Génère la réponse en streaming: produit chaque fragment de texte au
    fur et à mesure que Groq le génère, au lieu d'attendre la réponse complète.
    """
    try:
        stream=user.chat.completions.create(
            model=GROQ_CHAT_MODEL,
            messages=messages,
            stream=True
        )
        
        for chunk in stream:
            content=chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        logger.error(f"Échec de la génération (stream):{e}")
        raise

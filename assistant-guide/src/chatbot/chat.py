from src.chatbot.memory import ConversationMemory
from src.rag.retriever import retrieve_context, format_context
from src.rag.prompt import build_prompt, build_rewrite_prompt
from src.rag.generator import generate_answer
from src.utils.logger import get_logger
from src.rag.generator import generate_answer, generate_answer_stream

logger=get_logger(__name__)

def _format_history(exchanges:list[dict]):
    """Transforme une liste d'échanges en texte lisible pour le prompt de reformulation."""
    lines=[]
    for msg in exchanges:
        role="Utilisateur" if msg["role"]=="user" else "Assistant"
        lines.append(f"{role}:{msg['content']}")
    return "\n".join(lines) if lines else "(aucun histroique)"
        
class ChatSession:
    """
    Orchestre une session de converstion: reformulation de la question
    si besoin, retrieval, génération, mise à jour de l'historique.
    """
    
    def __init__(self, top_k:int=5, rewrite_threshold:int=1):
        self.memory=ConversationMemory()
        self.top_k=top_k
        self.rewrite_threshold=rewrite_threshold
    
    def _maybe_rewrite_query(self, query:str):
        """
        Reformule la question en question autonome si un historique existe,
        pour que le retriever ait assez de contexte (ex: "et pour l'hébergement?").
        """    
        recent=self.memory.get_recent_exchanges(n=2)
        if len(recent)<self.rewrite_threshold*2:
            return query
        
        history_text=_format_history(recent)
        rewrite_messages=build_rewrite_prompt(query, history_text)
        rewritten=generate_answer(rewrite_messages).strip()
        
        if rewritten and rewritten!=query:
            logger.info(f"Question refomulée: {query!r}->{rewritten!r}")
            return rewritten or query
        
    def ask(self, query:str):
        """ 
        Traite une question utilisateur de bout en bout:
        reformulation -> retrieval -> génération -> mise à jour historique.
        """
        search_query=self._maybe_rewrite_query(query)
        
        chunks=retrieve_context(search_query, top_k=self.top_k)
        context=format_context(chunks)
        
        messages=build_prompt(query, context)
        # On injecte l'historique récent dans les messages pour la génération finale
        recent=self.memory.get_recent_exchanges(n=3)
        full_messages=[messages[0]] + recent + [messages[1]]
        
        answer=generate_answer(full_messages)
        
        self.memory.add_user_message(query)
        self.memory.add_assistant_message(answer)
        
        return answer
    
    def ask_stream(self, query:str):
        """ 
        Produit la réponse fragment par fragment, puis met à jour la mémoire une fois le flux terminé.
        """
        search_query=self._maybe_rewrite_query(query)
        
        chunks=retrieve_context(search_query, top_k=self.top_k)
        context=format_context(chunks)
        
        messages=build_prompt(query, context)
        recent=self.memory.get_recent_exchanges(n=3)
        full_messages=[messages[0]] + recent + [messages[1]]
        
        full_anwer=""
        for fragment in generate_answer_stream(full_messages):
            full_anwer+=fragment
            yield fragment
            
        self.memory.add_user_message(query)
        self.memory.add_assistant_message(full_anwer)
        
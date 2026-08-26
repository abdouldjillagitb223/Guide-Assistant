class ConversationMemory:
    """
    Gère l'historique conversationnel en mémoire (une session=une instance).
    Ne fait pas de persistance disque.
    """
    
    def __init__(self, max_turns:int=10):
        self.max_turns=max_turns
        self.history:list[dict]=[]
        
    def add_user_message(self, content:str):
        self.history.append({"role":"user", "content":content})
        self.__trim()
        
    def _trim(self):
        """Garde seulement les derniers échanges (max_turns paires user/assistant)."""
        max_messages=self.max_turns*2
        if len(self.history)>max_messages:
            self.history=self.history[-max_messages:]
    
    def get_recent_exchanges(self, n:int=3):
        """Rétourne les n derniers échanges, utile pour la reformulation de requête."""        
        return self.history[-(n*2):]
    
    def clear(self):
        self.history=[]
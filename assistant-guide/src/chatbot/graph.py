from typing import TypedDict
from langgraph.graph import StateGraph, END

from src.rag.retriever import retrieve_context, format_context
from src.rag.prompt import build_prompt, build_rewrite_prompt
from src.rag.generator import generate_answer
from src.chatbot.memory import ConversationMemory
from src.config import TOP_K
from src.utils.logger import get_logger

logger=get_logger(__name__)

REWRITE_THRESHOLD=1

class ChatState(TypedDict):
    query:str
    search_query:str
    history:list[dict]
    context:str
    chunks:list[dict]
    answer:str


def _format_history(exchanges:list[dict]):
    lines=[]
    for msg in exchanges:
        role="Utilisateur" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}:{msg['content']}")
    return "\n".join(lines) if lines else "(aucun historique)"


def rewrite_query_node(state:ChatState):
    history= state["history"]
    if len(history) < REWRITE_THRESHOLD*2:
        return {**state, "search_query": state["query"]}
    
    history_text=_format_history(history[-(REWRITE_THRESHOLD*2):])
    rewrite_messages=build_rewrite_prompt(state["query"], history_text)
    rewritten=generate_answer(rewrite_messages).strip()
    
    if rewritten and rewritten != state["query"]:
        logger.info(f"Question reformulée: {state['query']!r} -> {rewritten!r}")
        return {**state, "search_query": rewritten}
    
    return {**state, "search_query": state["query"]}


def retrieve_node(state: ChatState):
    chunks= retrieve_context(state["search_query"], top_k=TOP_K)
    context=format_context(chunks)
    return {**state, "chunks":chunks, "context":context}


def generate_node(state: ChatState):
    messages=build_prompt(state["query"], state["context"])
    full_messages=[messages[0]] + state["history"] + [messages[1]]
    answer=generate_answer(full_messages)
    return {**state, "answer":answer}


def build_graph():
    workflow=StateGraph(ChatState)
    
    workflow.add_node("rewrite_query", rewrite_query_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    
    workflow.set_entry_point("rewrite_query")
    workflow.add_edge("rewrite_query", "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate",END)
    
    return workflow.compile()

chat_graph=build_graph()


class GraphChatSession:
    """
    Équivalent de ChatSession mais piloté par le graphe LangGraph. 
    Garde la même mémoire conversationnelle par session. 
    """
    
    def __init__(self, top_k:int=TOP_K):
        self.memory=ConversationMemory()
        self.top_k=top_k
    
    
    def ask(self, query:str):
        recent=self.memory.get_recent_exchanges(n=3)
        initial_state:ChatState={
            "query":query,
            "search_query":query,
            "history":recent,
            "context":"",
            "chunks":[],
            "answer":"",
        }
        final_state=chat_graph.invoke(initial_state)
        answer=final_state["answer"]
        
        self.memory.add_assistant_message(query)
        self.memory.add_assistant_message(answer)
        return answer
    
    
    def ask_with_trace(self, query:str):
        """ 
        Comme ask(), mais retourne aussi l'état final complet (utile pour afficher les sources/ le débug dans Chainlit).        
        """
        
        recent= self.memory.get_recent_exchanges(n=3)
        initial_state: ChatState={
            "query":query,
            "search_query": query,
            "history":recent,
            "context":"",
            "chunks":[],
            "answer":"",
        }
        final_state=chat_graph.invoke(initial_state)
        
        self.memory.add_user_message(query)
        self.memory.add_assistant_message(final_state["answer"])
        return final_state
    

if __name__=="__main__":
    session=GraphChatSession()
    print("=== Tour 1 ===")
    print(session.ask("Quels services de cybersécurité propose Jokers Company?"))
    print("\n=== Tour 2 (suivi) ===")
    print(session.ask("Et pour l'hébergement, vous proposez quoi?"))
        
        
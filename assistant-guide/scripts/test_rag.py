import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rag import retrieve_context, build_prompt, generate_answer
from src.rag.retriever import format_context

def ask(query:str):
    print(f"=== Question: {query} ===\n")
    
    chunks=retrieve_context(query, top_k=5)
    context=format_context(chunks)
    
    print("--- Contexte récupéré ---")

    for c in chunks:
        print(f"- {c['metadata']['section_heading']} (distance:{c['distance']:.3f})")
    print()
    
    messages=build_prompt(query, context)
    answer=generate_answer(messages)
    
    print("--- Réponse générée ---") 
    print(answer)
    print()

if __name__=="__main__":
    ask("Quels services de cybersécurité propose  Jokers Company?")   
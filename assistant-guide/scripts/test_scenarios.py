import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname("__file__"), "..")))

from src.chatbot import ChatSession

def run_scenario(title: str, questions:list[str]):
    print(f"\n{'='*60}")
    print(f"SCÉNARIO: {title}")
    print('='*60)
    
    session=ChatSession()
    for i, q in enumerate(questions, 1):
        print(f"\n--- Tour {i} ---")
        print(f"Q: {q}")
        answer=session.ask(q)
        print(f"R: {answer}")
    
# Scénario 1: question totalement hors-sujet
run_scenario("Hors-sujet", [
    "Quelle est la recette de la tarte tatin?",
])

# Scénario 2: sujet présent, mais détail précis absent du contexte
run_scenario("Détail absent (prix)", [
    "Combien coûte votre pack INFOGÉRANCE?"
])

# Scénario 3: conversation à 3 tours, sujets différents
run_scenario("Conversation multi-tours", [
    "Qui est Jokers Company?",
    "Dans quels pays êtes-vous présents?",
    "Et comment je peux vous contacter?",
])
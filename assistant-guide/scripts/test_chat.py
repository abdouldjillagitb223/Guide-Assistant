import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.chatbot import ChatSession

session=ChatSession()

print("=== Tour 1 ===")
print(session.ask("Quels services de cybersécurité propose Jokers Company?"))

print("\n=== Tour 2 (suivi) ===")
print(session.ask("Et pour l'hébergement, vous proposez quoi?"))
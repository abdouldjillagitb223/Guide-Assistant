import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from src.chatbot import ChatSession
from src.chatbot.memory import ConversationMemory


def test_conversation_memory_ajoute_et_recupere():
    memory = ConversationMemory()
    memory.add_user_message("Bonjour")
    memory.add_assistant_message("Bonjour, comment puis-je vous aider ?")
    assert len(memory.history) == 2


def test_conversation_memory_respecte_max_turns():
    memory = ConversationMemory(max_turns=2)
    for i in range(5):
        memory.add_user_message(f"Message {i}")
        memory.add_assistant_message(f"Réponse {i}")
    assert len(memory.history) == 4  # 2 tours max = 4 messages


@pytest.mark.integration
def test_hors_sujet_refuse_poliment():
    session = ChatSession()
    reponse = session.ask("Quelle est la recette de la tarte tatin ?")
    assert "Jokers Company" in reponse or "ne peux pas" in reponse.lower()


@pytest.mark.integration
def test_info_absente_repond_honnetement():
    session = ChatSession()
    reponse = session.ask("Combien coûte votre pack INFOGÉRANCE ?")
    assert "pas disponible" in reponse.lower() or "contactez" in reponse.lower()


@pytest.mark.integration
def test_question_cybersecurite_mentionne_le_sujet():
    session = ChatSession()
    reponse = session.ask("Quels services de cybersécurité proposez-vous ?")
    assert "sécurité" in reponse.lower() or "firewall" in reponse.lower()
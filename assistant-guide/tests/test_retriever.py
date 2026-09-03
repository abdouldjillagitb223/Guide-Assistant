import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from src.rag.retriever import retrieve_context, format_context


@pytest.mark.integration
def test_retrieve_context_retourne_des_resultats():
    resultats = retrieve_context("cybersécurité", top_k=5)
    assert len(resultats) > 0
    assert "text" in resultats[0]
    assert "metadata" in resultats[0]


@pytest.mark.integration
def test_retrieve_context_trouve_la_section_cybersecurite():
    resultats = retrieve_context("cybersécurité", top_k=5)
    headings = [r["metadata"]["section_heading"] for r in resultats]
    assert any("écurité" in h or "yber" in h for h in headings)


def test_format_context_gere_liste_vide():
    resultat = format_context([])
    assert "Aucune information" in resultat


def test_format_context_numerote_les_sources():
    chunks = [
        {"text": "Contenu A", "metadata": {"section_heading": "Section A"}},
        {"text": "Contenu B", "metadata": {"section_heading": "Section B"}},
    ]
    resultat = format_context(chunks)
    assert "[Source1" in resultat
    assert "[Source2" in resultat
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion.chunker import group_blocks_by_section, chunk_page


def _sample_blocks():
    return [
        {"type": "text", "level": None, "text": "Accueil"},
        {"type": "heading", "level": 4, "text": "Cyber Sécurité"},
        {"type": "text", "level": None, "text": "Mise en service et maintien d'équipements de sécurité."},
        {"type": "heading", "level": 4, "text": "Infrastructures reseaux"},
        {"type": "text", "level": None, "text": "Nous concevons des architectures sécurisées."},
    ]


def test_group_blocks_by_section_cree_une_section_par_titre():
    sections = group_blocks_by_section(_sample_blocks())
    headings = [s["heading"] for s in sections]
    assert "Cyber Sécurité" in headings
    assert "Infrastructures reseaux" in headings


def test_group_blocks_by_section_regroupe_le_bon_contenu():
    sections = group_blocks_by_section(_sample_blocks())
    cyber_section = next(s for s in sections if s["heading"] == "Cyber Sécurité")
    assert any("équipements de sécurité" in t for t in cyber_section["texts"])


def test_chunk_page_produit_un_chunk_par_section_courte():
    chunks = chunk_page(_sample_blocks())
    headings = [c["heading"] for c in chunks]
    assert "Cyber Sécurité" in headings
    assert "Infrastructures reseaux" in headings


def test_chunk_page_texte_contient_le_heading():
    chunks = chunk_page(_sample_blocks())
    cyber_chunk = next(c for c in chunks if c["heading"] == "Cyber Sécurité")
    assert cyber_chunk["text"].startswith("Cyber Sécurité")
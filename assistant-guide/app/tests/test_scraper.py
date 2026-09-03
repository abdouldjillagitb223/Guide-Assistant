import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scraper.cleaner import clean_text, remove_duplicate_lines, normalize_whitespace, fix_encoding
from src.scraper.crawler import is_internal_link
from ftfy import fix_text


def test_fix_text_repare_mojibake():
    texte_casse = "Câ€™est pour cela"
    resultat = fix_text(texte_casse)
    assert "'" in resultat
    assert "â€™" not in resultat


def test_remove_duplicate_lines_supprime_repetitions():
    texte = "Accueil\nContact\nAccueil"
    resultat = remove_duplicate_lines(texte)
    assert resultat.count("Accueil") == 1


def test_normalize_whitespace_reduit_sauts_de_ligne():
    texte = "Ligne 1\n\n\n\nLigne 2"
    resultat = normalize_whitespace(texte)
    assert "\n\n\n" not in resultat

def test_clean_text_corrige_le_mojibake():
    """Vérifie que clean_text applique bien la correction d'encodage (régression du bug fix_text)."""
    texte_casse = "Câ€™est pour cela"
    resultat = clean_text(texte_casse)
    assert "â€™" not in resultat  

def test_clean_text_pipeline_complet():
    texte = "Accueil\nAccueil\n© 2024 Jokers Company\nNos services incluent..."
    resultat = clean_text(texte)
    assert "Nos services incluent" in resultat
    assert resultat.count("Accueil") <= 1


def test_is_internal_link_detecte_meme_domaine():
    assert is_internal_link("https://www.jokerscompany.com/contact", "https://www.jokerscompany.com/")


def test_is_internal_link_rejette_domaine_externe():
    assert not is_internal_link("https://jokers-hosting.com/", "https://www.jokerscompany.com/")
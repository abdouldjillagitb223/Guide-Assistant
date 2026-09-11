import re
from ftfy import fix_text

# Motifs fréquents à filtrer (menus, footer, mentions légales...)
NOISE_PATTERNS=[
    r"©\s*\d{4}.*",
    r"tous droits réservés",
    r"mentions légales",
    r"politique de confidentialité",
    r"accepter les cookies",
]

def remove_noise_lines(text:str):
    """Supprime les lignes correspondant à du bruit connu (footer, cookies, etc...)."""
    lines=text.split("\n")
    cleaned=[]
    for line in lines:
        line_lower=line.lower().strip()
        if not line_lower:
            continue
        if any(re.search(pattern, line_lower) for pattern in NOISE_PATTERNS):
            continue
        cleaned.append(line.strip())
    return "\n".join(cleaned)

def remove_duplicate_lines(text:str):
    """Supprime les lignes répétées consécutuivement (souvent des éléments de menu)."""
    lines=text.split("\n")
    result=[]
    seen=set()
    for line in lines:
        if line not in seen:
            result.append(line)
            seen.add(line)
    return "\n".join(result)

def normalize_whitespace(text:str):
    """Réduit les espaces/sautes de ligne multiples."""
    text=re.sub(r"[\t]+", " ", text)
    text=re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def clean_text(raw_text:str):
    """Pipeline complet de nettoyage appliqué au texte extrait d'une page."""
    text=fix_text(raw_text)
    text=remove_noise_lines(text)
    text=remove_duplicate_lines(text)
    text=normalize_whitespace(text)
    return text

def clean_block_text(text:str):
    """Applique la correction d'encodage et normalise un texte de bloc (titre ou paragraphe)."""
    text=fix_text(text)
    text=normalize_whitespace(text)
    return text
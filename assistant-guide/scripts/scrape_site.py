import json
import os
import sys
from ftfy import fix_text 
from urllib.parse import urlparse

# Permet d'exécuter le script depuis la racine du projet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scraper import crawl_site, parse_page, clean_text
from src.config import SITE_BASE_URL, RAW_DATA_DIR
from src.utils.logger import get_logger

logger=get_logger(__name__)


def slugify(url:str):
    """Transforme une URL en nom de fichier lisible."""
    path=urlparse(url).path.strip("/")
    if not path:
        return "accueil"
    return path.replace("/", "-")

def main():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    logger.info(f"Début du scraping depuis {SITE_BASE_URL}")
    pages=crawl_site(SITE_BASE_URL, max_pages=50)
    
    for url, html in pages.items():
        parsed=parse_page(url, html)
        parsed["clean_text"]=clean_text(parsed["raw_text"])

        filename=slugify(url)+ ".json"
        filepath=os.path.join(RAW_DATA_DIR, filename)

        with open(filepath,"w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
    logger.info(f"Terminé. {len(pages)} pages sauvegardées dans {RAW_DATA_DIR}")

if __name__== "__main__":
    main()



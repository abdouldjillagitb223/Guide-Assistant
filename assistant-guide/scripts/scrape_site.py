import json
import os
import sys
from ftfy import fix_text 
from urllib.parse import urlparse

# Permet d'exécuter le script depuis la racine du projet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scraper import crawl_site, parse_page, clean_text
from src.config import SITE_BASE_URLS, RAW_DATA_DIR
from src.utils.logger import get_logger

logger=get_logger(__name__)


def slugify(url:str):
    """Transforme une URL en nom de fichier lisible"""
    parsed=urlparse(url)
    domain=parsed.netloc.replace("www.","").replace(".", "-")
    path=parsed.path.strip("/")
    slug=path.replace("/", "-") if path else "accueil"
    return f"{domain}__{slug}"

def main():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    total_pages=0
  
    
    for site_base_url in SITE_BASE_URLS:
        logger.info(f"Début du scraping depuis {site_base_url}")
        pages=crawl_site(site_base_url, max_pages=50)
        
        for url, html in pages.items():
            parsed=parse_page(url, html)
            parsed["clean_text"]=clean_text(parsed["raw_text"])

            filename=slugify(url)+ ".json"
            filepath=os.path.join(RAW_DATA_DIR, filename)

            with open(filepath,"w", encoding="utf-8") as f:
                json.dump(parsed, f, ensure_ascii=False, indent=2)
        
        logger.info(f"{site_base_url}:{len(pages)} pages sauvegardées.")
        total_pages+=len(pages)
    
    logger.info(f"Terminé. {total_pages} pages sauvegardées dans {RAW_DATA_DIR}")

if __name__== "__main__":
    main()



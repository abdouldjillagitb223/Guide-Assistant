import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from src.utils.logger import get_logger
from src.config import SITE_BASE_URL

logger=get_logger(__name__)

HEADERS={
    "User-Agent":"JokersCompany-RAG-Bot/1.0 (+contact:abdoulaye.djilla@jokerscompany.com)"
}

def is_internal_link(url:str, base_url:str):
    """Vérifie que le lien pointe bien vers le même domaine (pas de scraping externe)."""
    return urlparse(url).netloc in ("", urlparse(base_url).netloc)

def fetch_page(url:str, timeout:int=10):
    """Récupère le HTML d'une page.Retourne None en cas d'échec"""
    try:
        response=requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        return response.text
    except requests.RequestException as e:
        logger.error(f"Échec récupération {url}:{e}")
        return None

def discover_links(html:str, current_url:str, base_url:str):
    """Extrait tous les liens internes présents dans une page."""
    soup=BeautifulSoup(html,"html.parser")
    links=set()
    skip_extensions=(".jpg", ".jpeg", ".png", ".gif", ".svg", ".pdf", ".css", ".js")
    
    for tag in soup.find_all("a", href=True):
        href=tag["href"].strip()
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue
        if href.lower().endswith(skip_extensions):
            continue
        
        full_url=urljoin(current_url, href)
        full_url=full_url.split("#")[0]
        if is_internal_link(full_url, base_url):
            links.add(full_url)
    
    return links

def crawl_site(start_url:str=SITE_BASE_URL, max_pages:int=50):
    """
    Parcourt le site en largeur (BFS) à partir de start_url.
    Retourne un dictionnaire:{url:html_brut}.
    """
    visited:set[str]=set()
    to_visit:set[str]={start_url}
    pages:dict[str, str]={}
    
    while to_visit and len(visited)< max_pages:
        url=to_visit.pop()
        if url in visited:
            continue
        visited.add(url)
        
        logger.info(f"Scraping:{url}")
        html=fetch_page(url)
        if html is None:
            continue
        
        pages[url]=html
        new_links=discover_links(html, url, start_url)
        to_visit.update(new_links-visited)
    logger.info(f"Scraping terminé:{len(pages)} pages récupérées.")
    return pages
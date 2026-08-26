from bs4 import BeautifulSoup

HEADING_TAGS=["h1", "h2", "h3", "h4", "h5", "h6"]
CONTENT_TAGS=["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"]

def parse_page(url:str, html:str):
    """
    Transforme le HTML brut en structure exploitable: 
    titre, contenu principal, liens, éventuelle catégorie.
    """
    
    soup=BeautifulSoup(html, "html.parser")
    
    title_tag=soup.find("title")
    title=title_tag.get_text(strip=True) if title_tag else ""
    
    h1_tag=soup.find("h1")
    heading=h1_tag.get_text(strip=True) if h1_tag else title
    
    main=soup.find("main") or soup.find("article") or soup.find("body")
    blocks=[]
    if main:
        for tag in main.find_all(CONTENT_TAGS):
            text=tag.get_text(separator=" ", strip=True)
            if not text:
                continue
            blocks.append({
                "type":"heading" if tag.name in HEADING_TAGS else "text",
                "level": int(tag.name[1]) if tag.name in HEADING_TAGS else None,
                "text":text,
            })  
                
    links=[a["href"] for a in soup.find_all("a", href=True)]
    
    return{
        "url":url,
        "title":title,
        "heading":heading,
        "blocks":blocks,
        "raw_text":main.get_text(separator="\n", strip=True) if main else "",
        "links":links,
    }
    
    
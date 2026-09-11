from src.config import  CHUNK_SIZE, CHUNK_OVERLAP
from src.scraper.cleaner import clean_block_text

def group_blocks_by_section(blocks:list[dict]):
    """
    Regroupe les blocs en sections: chaque section commence par un titre
    (heading) et contient tout le texte qui suit jusqu'au titre suivant.
    Le contenu avant le premier titre forme une section "Introduction".
    """
    sections=[]
    current_section={"heading":"Introduction", "level":0, "texts":[]}
    
    for block in blocks:
        text=clean_block_text(block["text"])
        if not text:
            continue
        
        if block["type"]=="heading":
            # On clôt la section précédente si elle contient du contenu
            if current_section["texts"]:
                sections.append(current_section)
            current_section={"heading":text, "level":block["level"], "texts":[]}
        else:
            current_section["texts"].append(text)
            
    if current_section["texts"]:
        sections.append(current_section)
    
    return sections

def split_long_section(heading:str, texts:list[str], chunk_size:int, chunk_overlap:int):
    """
    Sous-découpe une section trop longue en plusieurs chunks, avec chevauchement.
    """
    chunks=[]
    current, current_len=[], 0
     
    for text in texts:
        if current_len+len(text)>chunk_size and current:
            chunks.append(f"{heading}\n"+"\n".join(current))
            overlap, overlap_len=[], 0
            for t in reversed(current):
                if overlap_len+len(t)>chunk_overlap:
                    break
                overlap.insert(0, t)
                overlap_len+=len(t)
            current, current_len=overlap, overlap_len
        current.append(text)
        current_len+=len(text)
    
    if current:
        chunks.append(f"{heading}\n"+"\n".join(current))
    
    return chunks

def chunk_page(
    blocks:list[dict],
    chunk_size:int=CHUNK_SIZE,
    chunk_overlap:int=CHUNK_OVERLAP, 
):
    """
    Découpe une page en chunks par section sémantique (basée sur les titres HTML).
    Retourne une liste de dicts {heading, text} - un ou plusieurs chunks par section
    selon sa longueur. 
    """
    sections=group_blocks_by_section(blocks)
    all_chunks=[]
    
    for section in sections:
        full_text="\n".join(section["texts"])
        if len(full_text)<= chunk_size:
            all_chunks.append({
                "heading": section["heading"],
                "text":f"{section['heading']}\n{full_text}"
            })
        else:
            for chunk_text in split_long_section(
                section["heading"], section["texts"], chunk_size, chunk_overlap
            ):
                all_chunks.append({"heading":section["heading"], "text":chunk_text})
    
    return all_chunks
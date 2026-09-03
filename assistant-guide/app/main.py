from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import uuid

from src.chatbot import ChatSession
from src.utils.logger import get_logger

logger=get_logger(__name__)

app=FastAPI(title="Jokers Company - Chatbot API")

# Autorise le widget (hébergé sur jokerscompany.com) à appeler cette API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"]
)

sessions:dict[str, ChatSession]={}

class ChatRequest(BaseModel):
    message:str
    session_id:str | None=None

class ChatResponse(BaseModel):
    reply:str
    session_id:str
    
@app.post("/chat/stream")
def chat_stream(request:ChatRequest):
    session_id=request.session_id or str(uuid.uuid4())
    
    if session_id not in sessions:
        sessions[session_id]=ChatSession()
        
    session=sessions[session_id]
    
    def event_generator():
        header=json.dumps({"session_id": session_id})
        yield f"{header}\n"
        try:
            for fragment in session.ask_stream(request.message):
                yield fragment
        except Exception as e:
            logger.error(f"Erreur streaming:{e}")
            yield "\n[Erreur lors de la génération de la réponse]"
    return StreamingResponse(event_generator(), media_type="text/plain")

@app.get("/health")
def health():
    return {"status":"ok"}
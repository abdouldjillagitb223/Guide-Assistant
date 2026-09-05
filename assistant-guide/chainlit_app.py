import chainlit as cl

from src.chatbot.graph import GraphChatSession
from src.utils.logger import get_logger

logger=get_logger(__name__)

@cl.on_chat_start
async def on_chat_start():
    # Une session GraphChatSession par utilisateur connecté (mémoire isolée)
    cl.user_session.set("chat_session", GraphChatSession())
    
    
    await cl.Message(
        content=(
            "Bonjour 👋! Je suis l'assistant virtuel de **Jokers Company**."
            "Á quoi puis-je vous aider?"
        )
    ).send()
    
    
@cl.on_message
async def on_message(message:cl.Message):
        chat_session:GraphChatSession=cl.user_session.get("chat_session")
        
        thinking=cl.Message(content="")
        await thinking.send()
        
        try:
            final_state=chat_session.ask_with_trace(message.content)
            
        except Exception as e:
            logger.error(
                f"Erreur lors du traitement de la question: {e}",
                exc_info=True
            )
            
            thinking.content=(
                "Désolé, une erreur est survenue pendant le traitement de votre"
                "question. Merci de réessayer dans un instant."
            )
            
            await thinking.update()
            return
        
        answer=final_state["answer"]
        chunks=final_state.get("chunks", [])
        
        thinking.content= answer
        await thinking.update()
        
        # Afficher les sources utilisées, si disponibles, comme éléments Chainlit 
        if chunks:
            sources_text="\n".join(
                f"- {c['metadata'].get('section_heading', 'Section')}"
                f"({c['metadata'].get('url', '')})"
                for c in chunks
            )
            
            await cl.Message(
                content=f"**Source consultées: **\n{sources_text}",
                author="system",
            ).send()
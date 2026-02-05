from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.groq_service import get_groq_response, clear_memory

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply, in_w, out_w = get_groq_response(request.message, request.role)
    return ChatResponse(
        reply=reply,
        input_words=in_w,
        output_words=out_w
    )

@router.post("/clear")
def clear_chat():
    clear_memory()
    return {"status": "cleared"}

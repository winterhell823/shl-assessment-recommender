from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
from app.agent.chat_agent import ChatAgent

router = APIRouter()
agent = ChatAgent()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return agent.handle_chat(request)
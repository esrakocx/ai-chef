from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, ChatHistory
from app.schemas import ChatRequest, ChatResponse
from app.utils.auth_utils import get_current_user
from app.services.gemini_service import chat_with_chef

router = APIRouter(prefix="/api/chat", tags=["Mutfak Asistanı"])


@router.post("/message", response_model=ChatResponse)
def send_message(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == current_user.id)
        .order_by(ChatHistory.created_at.desc())
        .limit(5)
        .all()
    )

    history_list = [
        {"prompt": h.prompt, "response": h.response}
        for h in reversed(history)
    ]

    response_text = chat_with_chef(
        message=chat_request.message,
        recipe_context=chat_request.recipe_context,
        chat_history=history_list,
    )

    chat_entry = ChatHistory(
        user_id=current_user.id,
        prompt=chat_request.message,
        response=response_text,
    )
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)

    return ChatResponse(response=response_text, created_at=chat_entry.created_at)


@router.get("/history", response_model=List[ChatResponse])
def get_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == current_user.id)
        .order_by(ChatHistory.created_at.desc())
        .limit(20)
        .all()
    )
    return [
        ChatResponse(response=h.response, created_at=h.created_at)
        for h in history
    ]


@router.delete("/clear-history")
def clear_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Sohbet geçmişi temizlendi"}

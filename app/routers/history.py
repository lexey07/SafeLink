from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.url_check import UrlCheck
from app.dependencies import get_current_user
from app.schemas.history_schema import HistoryResponse

router = APIRouter()

@router.get("/history", response_model=list[HistoryResponse])
def get_history(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = (
        db.query(UrlCheck)
        .filter(UrlCheck.username == current_user)
        .order_by(UrlCheck.created_at.desc())
        .all()
    )

    return history
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.url_check import UrlCheck
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/history")
def get_history(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(UrlCheck).filter(
        UrlCheck.username == current_user
    ).all()

    return history
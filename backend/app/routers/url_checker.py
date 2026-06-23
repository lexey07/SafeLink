from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.url_check import UrlCheck
from app.database.session import get_db
from app.schemas.url_schema import UrlSchema
from app.dependencies import get_current_user
from app.analyzers.url_analyzer import analyze_url
from app.qwen_service import explain_url

router = APIRouter()

print("URL ROUTER LOADED")


@router.post("/check-url")
def check_url(
    data: UrlSchema,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == current_user
    ).first()

    if not user:
        return {
            "message": "Пользователь не найден"
        }

    if not user.is_premium and user.checks_left <= 0:
        return {
            "message": "Лимит бесплатных проверок исчерпан. Купите Premium."
        }

    if not user.is_premium:
        user.checks_left -= 1
        db.commit()

    analysis = analyze_url(data.url)

    status = analysis["status"]
    risk_score = analysis["risk_score"]
    reasons = analysis["reasons"]

    ai_explanation = explain_url(
        data.url,
        status,
        risk_score,
        reasons
    )

    check = UrlCheck(
        url=data.url,
        status=status,
        username=current_user
    )

    db.add(check)
    db.commit()
    db.refresh(check)

    return {
        "url": data.url,
        "status": status,
        "risk_score": risk_score,
        "reasons": reasons,
        "ai_explanation": ai_explanation,
        "checks_left": user.checks_left,
        "premium": user.is_premium
    }
from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.url_check import UrlCheck
from app.schemas.url_schema import UrlSchema
from app.dependencies import get_current_user

router = APIRouter()

print("URL ROUTER LOADED")

@router.post("/check-url")
def check_url(
    data: UrlSchema,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == data.username
    ).first()

    print(dir(user))
    print(user)
    print(type(user))
    print(user.__dict__)

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

        suspicious_words = [
            "login",
            "verify",
            "bank",
            "paypal",
            "secure"
        ]

        status = "safe"

    for word in suspicious_words:
        if word in data.url.lower():
            status = "suspicious"
            break

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
        "checks_left": user.checks_left,
        "premium": user.is_premium
        }
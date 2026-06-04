from app.jwt_handler import create_access_token
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate
from app.models.user import User
from app.database.session import get_db
from app.security import hash_password
from app.schemas.login_schema import LoginSchema
from app.security import verify_password

router = APIRouter()

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    hashed_password = hash_password(user.password)
    print("HASH:", hashed_password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Пользователь зарегистрирован",
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }

@router.post("/login")
def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if not user:
        return {
            "message": "Пользователь не найден"
        }

    if not verify_password(
        data.password,
        user.password
    ):
        return {
            "message": "Неверный пароль"
        }

    token = create_access_token(
    {
        "username": user.username
    }
)

    return {
        "message": "Вход выполнен",
        "token": token,
        "username": user.username,
        "email": user.email
    }
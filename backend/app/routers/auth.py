import random
import os
import shutil
import uuid
from app.jwt_handler import create_access_token
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate
from app.models.user import User
from app.database.session import get_db
from app.schemas.login_schema import LoginSchema
from app.security import hash_password
from app.security import verify_password
from app.dependencies import get_current_user
from app.schemas.verify_schema import VerifySchema
from app.schemas.avatar_schema import AvatarSchema
from fastapi import UploadFile, File

router = APIRouter()

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    hashed_password = hash_password(user.password)
    print("HASH:", hashed_password)

    verification_code = str(
        random.randint(100000, 999999)
    )

    print(
        "EMAIL VERIFY CODE:",
        verification_code
    )

    new_user = User(
        username=user.nickname,
        nickname=user.nickname,
        email=user.email,
        password=hashed_password,
        avatar=None,
        verification_code=verification_code,
        email_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Код отправлен",
        "email": new_user.email
    }

@router.post("/login")
def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
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
    
    if not user.email_verified:
        return {
            "message": "Подтвердите Email"
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

@router.get("/me")
def get_me(
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

    return {
        "username": user.username,
        "nickname": user.nickname,
        "email": user.email,
        "avatar": user.avatar,
        "checks_left": user.checks_left,
        "is_premium": user.is_premium
    }

@router.post("/verify-email")
def verify_email(
    data: VerifySchema,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        return {
            "message": "Пользователь не найден"
        }

    if user.verification_code != data.code:
        return {
            "message": "Неверный код"
        }

    user.email_verified = True
    user.verification_code = None

    db.commit()

    token = create_access_token(
        {
            "username": user.username
        }
    )

    return {
        "message": "Email подтвержден",
        "token": token
    }

@router.post("/resend-code")
def resend_code(
    data: VerifySchema,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        return {
            "message": "Пользователь не найден"
        }

    verification_code = str(
        random.randint(100000, 999999)
    )

    user.verification_code = (
        verification_code
    )

    db.commit()

    print(
        "NEW EMAIL VERIFY CODE:",
        verification_code
    )

    return {
        "message": "Код отправлен"
    }

@router.post("/update-avatar")
def update_avatar(
    avatar: UploadFile = File(...),
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

    if not avatar.content_type.startswith("image/"):
        return {
            "message": "Можно загружать только изображения"
        }
    
    avatar.file.seek(0, 2)
    file_size = avatar.file.tell()
    avatar.file.seek(0)

    if file_size > 5 * 1024 * 1024:
        return {
            "message": "Максимальный размер изображения — 5 МБ"
        }

    extension = os.path.splitext(
        avatar.filename
    )[1]

    filename = (
        f"{uuid.uuid4()}{extension}"
    )

    upload_path = os.path.join(
        "uploads",
        "avatars",
        filename
    )

    print("CWD:", os.getcwd())
    print("UPLOAD PATH:", upload_path)
    print("EXISTS uploads:", os.path.exists("uploads"))
    print("EXISTS avatars:", os.path.exists(os.path.join("uploads", "avatars")))

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(
            avatar.file,
            buffer
        )

    user.avatar = (
        f"/uploads/avatars/{filename}"
    )

    db.commit()

    return {
        "message": "Аватар обновлен",
        "avatar": user.avatar
    }
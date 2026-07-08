from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth import AuthHandler, get_auth_handler

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_handler: AuthHandler = Depends(get_auth_handler),
) -> str:
    """
    Получает текущего пользователя из токена.
    Используется как dependency в роутерах.
    """
    try:
        return auth_handler.get_username(credentials.credentials)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
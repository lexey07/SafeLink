from datetime import datetime, timedelta
from jose import jwt
from typing import Dict, Any, Optional


class JwtHandler:
    """
    Обработчик JWT токенов.
    """
    
    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: Optional[str] = None,
        expire_days: int = 7
    ):
        self.secret_key = secret_key or "safelink_secret_key_2026"
        self.algorithm = algorithm or "HS256"
        self.expire_days = expire_days
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Создает JWT токен."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.expire_days)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Декодирует JWT токен."""
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
    
    def get_username(self, token: str) -> str:
        """Извлекает username из токена."""
        try:
            payload = self.decode_token(token)
            username = payload.get("username")
            if not username:
                raise ValueError("Неверный токен: отсутствует username")
            return username
        except jwt.JWTError as e:
            raise ValueError(f"Токен недействителен: {e}")


# ═══════════════════════════════════════════════════════════════
# СОХРАНЯЕМ ВСЕ СТАРЫЕ КОНСТАНТЫ И ФУНКЦИИ ДЛЯ СОВМЕСТИМОСТИ
# ═══════════════════════════════════════════════════════════════

SECRET_KEY = "safelink_secret_key_2026"
ALGORITHM = "HS256"

_jwt_handler = JwtHandler(secret_key=SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Обратная совместимость.
    Создает JWT токен.
    """
    return _jwt_handler.create_access_token(data)


def decode_token(token: str) -> Dict[str, Any]:
    """
    Обратная совместимость.
    Декодирует JWT токен.
    """
    return _jwt_handler.decode_token(token)


def get_jwt_handler() -> JwtHandler:
    """Возвращает экземпляр JwtHandler для DI."""
    return _jwt_handler
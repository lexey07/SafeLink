from passlib.context import CryptContext
from typing import Optional


class PasswordHasher:
    """
    Хеширование и верификация паролей.
    Использует bcrypt через passlib.
    """
    
    def __init__(self, schemes: Optional[list] = None):
        """
        Инициализация хешера.
        
        Args:
            schemes: Список схем хеширования (по умолчанию ["bcrypt"])
        """
        self._context = CryptContext(
            schemes=schemes or ["bcrypt"],
            deprecated="auto"
        )
    
    def hash(self, password: str) -> str:
        """
        Хеширует пароль.
        
        Args:
            password: Пароль в открытом виде
        
        Returns:
            Хешированный пароль
        """
        return self._context.hash(password)
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет пароль на соответствие хешу.
        
        Args:
            plain_password: Пароль в открытом виде
            hashed_password: Хешированный пароль
        
        Returns:
            True если пароль совпадает, иначе False
        """
        return self._context.verify(plain_password, hashed_password)


# ═══════════════════════════════════════════════════════════════
# ДЛЯ ОБРАТНОЙ СОВМЕСТИМОСТИ (чтобы старый код продолжал работать)
# ═══════════════════════════════════════════════════════════════

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Обратная совместимость.
    Хеширует пароль.
    """
    return _hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Обратная совместимость.
    Проверяет пароль на соответствие хешу.
    """
    return _hasher.verify(plain_password, hashed_password)


def get_password_hasher() -> PasswordHasher:
    """Возвращает экземпляр PasswordHasher для DI."""
    return _hasher

# Что изменилось:
#   1. Глобальный pwd_context → поле объекта
#   2. Функции → методы класса
#   3. Добавлена возможность указать схемы через конструктор
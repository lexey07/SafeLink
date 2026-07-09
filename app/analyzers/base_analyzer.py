from abc import ABC, abstractmethod
from urllib.parse import urlparse
from typing import Dict, List, Any


class BaseAnalyzer(ABC):
    """
    Базовый класс для всех анализаторов.
    Содержит общую логику: парсинг URL, добавление рисков, формирование результата.
    """
    
    def __init__(self):
        self._risk_score: int = 0
        self._reasons: List[str] = []
    
    @abstractmethod
    def analyze(self, url: str) -> Dict[str, Any]:
        """
        Анализирует URL и возвращает результат.
        Должен быть переопределен в каждом анализаторе.
        """
        pass
    
    def _extract_hostname(self, url: str) -> str:
        """Извлекает hostname из URL. Общий метод для всех анализаторов."""
        if "://" not in url:
            url = f"//{url}"
        parsed = urlparse(url)
        try:
            hostname = parsed.hostname
        except ValueError:
            return ""
        return (hostname or "").rstrip(".").lower()
    
    def _add_risk(self, score: int, reason: str) -> None:
        """Добавляет риск и причину."""
        self._risk_score += score
        if reason:
            self._reasons.append(reason)
    
    def _get_result(self, max_score: int = 100) -> Dict[str, Any]:
        """Возвращает итоговый результат с уникальными причинами."""
        return {
            "risk_score": min(self._risk_score, max_score),
            "reasons": list(dict.fromkeys(self._reasons))  # Удаляем дубликаты
        }
    
    def _reset(self) -> None:
        """Сбрасывает состояние анализатора (для переиспользования)."""
        self._risk_score = 0
        self._reasons = []

# Что изменилось:
#   1. Создан абстрактный базовый класс
#   2. Вынесена общая логика (_extract_hostname, _add_risk, _get_result)
#   3. Введен единый интерфейс через метод analyze()
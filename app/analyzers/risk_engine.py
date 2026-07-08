from typing import Dict, Any, Tuple, Set, List
from enum import Enum


class RiskStatus(str, Enum):
    """Статусы риска."""
    SAFE = "Безопасно"
    SUSPICIOUS = "Подозрительно"
    HIGH_RISK = "Высокий риск"
    DANGEROUS = "Опасно"


class RiskEngine:
    """
    Движок расчета рисков.
    Агрегирует результаты анализаторов: суммирует риски, фильтрует причины,
    определяет статус.
    """
    
    MAX_SCORE = 100
    
    def __init__(self):
        # Приоритеты причин (чем меньше число, тем выше приоритет)
        self._priority: Dict[str, int] = {
            "OpenPhish": 0,
            "имитирует бренд": 1,
            "Подмена символа": 2,
            "алфавитов": 3,
            "IP-адрес": 4,
            "не найден": 5,
        }
        
        # Критические причины (если есть хоть одна, банальные удаляются)
        self._critical: Tuple[str, ...] = (
            "имитирует бренд",
            "Подмена символа",
            "OpenPhish",
            "IP-адрес",
            "Punycode",
            "алфавитов",
            "редирект"
        )
        
        # Банальные причины (удаляются при наличии критических)
        self._banal: Tuple[str, ...] = (
            "Домен существует более года",
            "Домен существует и доступен в интернете"
        )
    
    def calculate_risk(self, *analyses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитывает итоговый риск на основе результатов анализаторов.
        
        Args:
            *analyses: Результаты анализаторов (dict с risk_score и reasons)
        
        Returns:
            Dict с status, risk_score, reasons
        """
        # Суммируем риски
        total_score = self._sum_risk_scores(analyses)
        total_score = min(total_score, self.MAX_SCORE)
        
        # Собираем уникальные причины
        all_reasons = self._collect_reasons(analyses)
        
        # Фильтруем банальные причины
        filtered_reasons = self._filter_reasons(all_reasons)
        
        # Сортируем по приоритету
        sorted_reasons = self._sort_reasons(filtered_reasons)
        
        return {
            "status": self._get_status(total_score),
            "risk_score": total_score,
            "reasons": sorted_reasons[:5]  # Только топ-5
        }
    
    def _sum_risk_scores(self, analyses: Tuple[Dict[str, Any], ...]) -> int:
        """Суммирует оценки риска из всех анализаторов."""
        return sum(a.get("risk_score", 0) for a in analyses)
    
    def _collect_reasons(self, analyses: Tuple[Dict[str, Any], ...]) -> Set[str]:
        """Собирает уникальные причины из всех анализаторов."""
        reasons: Set[str] = set()
        for analysis in analyses:
            for reason in analysis.get("reasons", []):
                if reason:
                    reasons.add(reason)
        return reasons
    
    def _filter_reasons(self, reasons: Set[str]) -> Set[str]:
        """
        Фильтрует банальные причины, если есть критические.
        
        Если есть хотя бы одна критическая причина, удаляем банальные.
        """
        has_critical = any(
            any(keyword in reason for keyword in self._critical)
            for reason in reasons
        )
        
        if has_critical:
            return {r for r in reasons if r not in self._banal}
        
        return reasons
    
    def _sort_reasons(self, reasons: Set[str]) -> List[str]:
        """Сортирует причины по приоритету."""
        def priority(reason: str) -> int:
            for keyword, score in self._priority.items():
                if keyword in reason:
                    return score
            return 100
        
        return sorted(reasons, key=priority)
    
    def _get_status(self, score: int) -> str:
        """Определяет статус на основе оценки риска."""
        if score == 0:
            return RiskStatus.SAFE.value
        if score <= 30:
            return RiskStatus.SUSPICIOUS.value
        if score <= 65:
            return RiskStatus.HIGH_RISK.value
        return RiskStatus.DANGEROUS.value


# ═══════════════════════════════════════════════════════════════
# ДЛЯ ОБРАТНОЙ СОВМЕСТИМОСТИ (чтобы старый код продолжал работать)
# ═══════════════════════════════════════════════════════════════

_engine = RiskEngine()


def calculate_risk(*analyses: Dict[str, Any]) -> Dict[str, Any]:
    """
    Обратная совместимость со старым кодом.
    Вызывает метод calculate_risk у синглтона RiskEngine.
    """
    return _engine.calculate_risk(*analyses)


def get_risk_engine() -> RiskEngine:
    """Возвращает экземпляр RiskEngine для DI."""
    return _engine
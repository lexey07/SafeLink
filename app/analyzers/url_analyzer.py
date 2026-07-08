import time
from typing import Dict, Any, Optional, List
import requests

from app.analyzers.structure_analyzer import StructureAnalyzer
from app.analyzers.similarity_analyzer import SimilarityAnalyzer
from app.analyzers.brand_similarity_analyzer import BrandSimilarityAnalyzer
from app.analyzers.reputation_analyzer import ReputationAnalyzer
from app.analyzers.domain_age_analyzer import DomainAgeAnalyzer
from app.analyzers.redirect_analyzer import RedirectAnalyzer
from app.analyzers.html_analyzer import HtmlAnalyzer
from app.analyzers.ip_analyzer import IpAnalyzer
from app.analyzers.trusted_domain_analyzer import TrustedDomainAnalyzer
from app.analyzers.risk_engine import RiskEngine, get_risk_engine


class UrlAnalyzer:
    """
    Главный анализатор URL.
    Оркестрирует работу всех анализаторов и агрегирует результаты.
    """
    
    def __init__(self):
        """Инициализация всех анализаторов."""
        self._analyzers = [
            StructureAnalyzer(),
            SimilarityAnalyzer(),
            BrandSimilarityAnalyzer(),
            ReputationAnalyzer(),
            DomainAgeAnalyzer(),
            RedirectAnalyzer(),
            HtmlAnalyzer(),
            IpAnalyzer(),
        ]
        self._trusted_analyzer = TrustedDomainAnalyzer()
        self._risk_engine = get_risk_engine()
    
    def analyze(self, url: str) -> Dict[str, Any]:
        """
        Выполняет полный анализ URL.
        
        Args:
            url: URL для анализа
        
        Returns:
            Результат анализа с status, risk_score, reasons
        """
        start_time = time.time()
        
        # 1. Проверка доверенного домена
        trusted_result = self._trusted_analyzer.analyze(url)
        is_trusted = trusted_result.get("trusted", False)
        
        # 2. Запуск всех анализаторов (ОДИН РАЗ!)
        results = []
        for analyzer in self._analyzers:
            result = analyzer.analyze(url)
            
            # Если домен доверенный — обнуляем риск
            if is_trusted and "risk_score" in result:
                result["risk_score"] = 0
            
            results.append(result)
        
        # 3. HTTP-запрос (если нужно)
        http_result = self._fetch_and_analyze_http(url)
        if http_result:
            results.append(http_result)
        
        # 4. Агрегация результатов
        final_result = self._risk_engine.calculate_risk(*results)
        
        print(f"URL analysis completed in {round(time.time() - start_time, 3)}s")
        return final_result
    
    def _fetch_and_analyze_http(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Выполняет HTTP-запрос и анализирует редиректы и HTML.
        
        Args:
            url: URL для запроса
        
        Returns:
            Результат анализа или None при ошибке
        """
        response = None
        try:
            normalized_url = url if "://" in url else f"https://{url}"
            response = requests.get(
                normalized_url,
                allow_redirects=True,
                timeout=2
            )
        except requests.RequestException:
            return None
        
        if not response:
            return None
        
        # Анализ редиректов
        redirect_result = RedirectAnalyzer().analyze(url, response)
        
        # Анализ HTML
        html_result = HtmlAnalyzer().analyze(url, response)
        
        # Агрегируем HTTP-результаты
        return self._risk_engine.calculate_risk(redirect_result, html_result)


# ═══════════════════════════════════════════════════════════════
# ДЛЯ ОБРАТНОЙ СОВМЕСТИМОСТИ (чтобы старый код продолжал работать)
# ═══════════════════════════════════════════════════════════════

_analyzer = UrlAnalyzer()


def analyze_url(url: str) -> Dict[str, Any]:
    """
    Обратная совместимость со старым кодом.
    Вызывает метод analyze у синглтона UrlAnalyzer.
    """
    return _analyzer.analyze(url)


def get_url_analyzer() -> UrlAnalyzer:
    """Возвращает экземпляр UrlAnalyzer для DI."""
    return _analyzer
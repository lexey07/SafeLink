from app.analyzers.base_analyzer import BaseAnalyzer
from typing import Dict, Any
from urllib.parse import urlparse
import requests


class RedirectAnalyzer(BaseAnalyzer):
    """Анализатор редиректов."""
    
    def analyze(self, url: str, response: requests.Response = None) -> Dict[str, Any]:
        self._reset()
        
        if not response:
            return self._get_result()
        
        original_hostname = self._extract_hostname(url)
        final_hostname = self._extract_hostname(response.url)
        
        if original_hostname and final_hostname:
            orig = self._normalize(original_hostname)
            final = self._normalize(final_hostname)
            
            if orig != final:
                self._add_risk(30, f"Обнаружен редирект на другой домен: {final_hostname}")
        
        return self._get_result()
    
    def _normalize(self, domain: str) -> str:
        if domain.startswith("www."):
            return domain[4:]
        return domain

# Что изменилось:
#   1. Функция → Класс
#   2. Убрана логика парсинга URL
#   3. Метод _normalize стал методом класса

#utfbuyfuyfuo
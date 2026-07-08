from app.analyzers.base_analyzer import BaseAnalyzer
from typing import Dict, Any
import requests


class HtmlAnalyzer(BaseAnalyzer):
    """Анализатор HTML-содержимого страницы."""
    
    def analyze(self, url: str, response: requests.Response = None) -> Dict[str, Any]:
        self._reset()
        
        if not response:
            return self._get_result()
        
        try:
            html = response.text[:50000].lower()
            if 'type="password"' in html:
                self._add_risk(15, "На странице обнаружено поле ввода пароля")
        except Exception:
            pass
        
        return self._get_result()

# Что изменилось:
#   1. Функция → Класс
#   2. Использует методы родителя
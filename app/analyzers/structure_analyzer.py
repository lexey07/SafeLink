from app.analyzers.base_analyzer import BaseAnalyzer
from ipaddress import ip_address
from typing import Dict, Any


class StructureAnalyzer(BaseAnalyzer):
    """Анализатор структуры URL."""
    
    def analyze(self, url: str) -> Dict[str, Any]:
        self._reset()
        hostname = self._extract_hostname(url)
        
        # HTTP вместо HTTPS
        if url.lower().startswith("http://"):
            self._add_risk(15, "Используется HTTP вместо HTTPS")
        
        # Длинная ссылка
        if len(url) > 75:
            self._add_risk(10, "Ссылка слишком длинная")
        
        # Длинный домен
        if hostname and len(hostname) > 40:
            self._add_risk(10, "Домен слишком длинный")
        
        # Много поддоменов
        if hostname and hostname.count(".") - 1 >= 2:
            self._add_risk(15, "Обнаружено много поддоменов")
        
        # Много точек
        if hostname and hostname.count(".") >= 4:
            self._add_risk(10, "Домен содержит слишком много точек")
        
        # Много дефисов
        if hostname and hostname.count("-") >= 3:
            self._add_risk(10, "Домен содержит много дефисов")
        
        # Двойной дефис
        if hostname and "--" in hostname:
            self._add_risk(10, "Обнаружен двойной дефис")
        
        # Много цифр
        if hostname and sum(c.isdigit() for c in hostname) >= 5:
            self._add_risk(10, "Домен содержит много цифр")
        
        # Символ @
        if "@" in url:
            self._add_risk(20, "Ссылка содержит символ @")
        
        # Локальный или приватный адрес
        if hostname and self._is_local_or_private(hostname):
            self._add_risk(25, "Ссылка указывает на локальный или приватный адрес")
        
        # Подозрительная TLD
        suspicious_tlds = {".xyz", ".top", ".click", ".shop", ".buzz", ".tk", ".cf", ".ml", ".gq"}
        if hostname and any(hostname.endswith(tld) for tld in suspicious_tlds):
            self._add_risk(15, "Используется подозрительная доменная зона")
        
        # URL-сокращатель
        shorteners = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly"}
        if hostname and any(hostname == s or hostname.endswith(f".{s}") for s in shorteners):
            self._add_risk(15, "Используется сервис сокращения ссылок")
        
        return self._get_result()
    
    def _is_local_or_private(self, hostname: str) -> bool:
        """Проверяет, является ли адрес локальным или приватным."""
        if hostname == "localhost":
            return True
        try:
            ip = ip_address(hostname)
            return ip.is_loopback or ip.is_private
        except ValueError:
            return False
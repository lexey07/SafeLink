from app.analyzers.base_analyzer import BaseAnalyzer
from typing import Dict, Any, Set
from datetime import datetime, timedelta
from socket import gethostbyname, gaierror
import requests


class ReputationAnalyzer(BaseAnalyzer):
    """Анализатор репутации домена (DNS + OpenPhish)."""
    
    def __init__(self):
        super().__init__()
        self._phishing_cache: Set[str] = set()
        self._last_update: datetime | None = None
        self._cache_ttl = timedelta(hours=1)
    
    def analyze(self, url: str) -> Dict[str, Any]:
        self._reset()
        hostname = self._extract_hostname(url)
        
        if not hostname:
            self._add_risk(50, "Не удалось определить доменное имя")
            return self._get_result()
        
        # DNS проверка
        if self._has_dns_record(hostname):
            self._reasons.append("Домен существует и доступен в интернете")
        else:
            self._add_risk(50, "Домен не найден в интернете")
        
        # Проверка OpenPhish
        if self._check_openphish(url):
            return {
                "risk_score": 100,
                "reasons": ["URL найден в базе известных фишинговых сайтов OpenPhish"]
            }
        
        return self._get_result()
    
    def _has_dns_record(self, hostname: str) -> bool:
        """Проверяет наличие DNS-записи."""
        try:
            gethostbyname(hostname)
            return True
        except gaierror:
            return False
    
    def _check_openphish(self, url: str) -> bool:
        """Проверяет URL в базе OpenPhish."""
        self._update_cache()
        return url.strip() in self._phishing_cache
    
    def _update_cache(self) -> None:
        """Обновляет кэш OpenPhish."""
        if self._last_update and datetime.now() - self._last_update < self._cache_ttl:
            return
        
        try:
            response = requests.get("https://openphish.com/feed.txt", timeout=10)
            if response.status_code == 200:
                self._phishing_cache = set(response.text.splitlines())
                self._last_update = datetime.now()
                print(f"OpenPhish cache updated: {len(self._phishing_cache)} URLs")
        except requests.RequestException:
            pass
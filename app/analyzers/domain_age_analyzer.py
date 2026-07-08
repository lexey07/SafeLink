from app.analyzers.base_analyzer import BaseAnalyzer
from typing import Dict, Any
from datetime import datetime, timezone
import whois
from socket import gethostbyname, gaierror


class DomainAgeAnalyzer(BaseAnalyzer):
    """Анализатор возраста домена через WHOIS."""
    
    def analyze(self, url: str) -> Dict[str, Any]:
        self._reset()
        hostname = self._extract_hostname(url)
        
        if not hostname:
            return self._get_result()
        
        # Проверяем, существует ли домен
        try:
            gethostbyname(hostname)
        except gaierror:
            return self._get_result()
        
        try:
            info = whois.whois(hostname)
            creation = info.creation_date
            
            if isinstance(creation, list):
                creation = creation[0]
            
            if not creation:
                return self._get_result()
            
            age_days = (datetime.now(timezone.utc) - creation.astimezone(timezone.utc)).days
            
            if age_days < 30:
                self._add_risk(40, "Домен зарегистрирован менее месяца назад")
            elif age_days < 180:
                self._add_risk(25, "Домен зарегистрирован менее 6 месяцев назад")
            elif age_days < 365:
                self._add_risk(10, "Домен зарегистрирован менее года назад")
            else:
                self._reasons.append("Домен существует более года")
        
        except Exception as e:
            print(f"WHOIS ERROR: {e}")
            return self._get_result()
        
        return self._get_result()
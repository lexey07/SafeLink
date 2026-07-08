from app.analyzers.base_analyzer import BaseAnalyzer
from typing import Dict, Any
from ipaddress import ip_address


class IpAnalyzer(BaseAnalyzer):
    """Анализатор IP-адресов в URL."""
    
    def analyze(self, url: str) -> Dict[str, Any]:
        self._reset()
        hostname = self._extract_hostname(url)
        
        if not hostname:
            return self._get_result()
        
        try:
            ip_address(hostname)
            self._add_risk(30, "В ссылке используется IP-адрес вместо домена")
        except ValueError:
            pass
        
        return self._get_result()
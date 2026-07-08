from app.analyzers.base_analyzer import BaseAnalyzer
from typing import Dict, Any


class TrustedDomainAnalyzer(BaseAnalyzer):
    """Анализатор доверенных доменов."""
    
    def __init__(self, trusted_file: str = "app/trusted_domains.txt"):
        super().__init__()
        self._trusted_file = trusted_file
    
    def analyze(self, url: str) -> Dict[str, Any]:
        self._reset()
        hostname = self._extract_hostname(url)
        
        try:
            with open(self._trusted_file, "r", encoding="utf-8") as f:
                trusted = {line.strip().lower() for line in f if line.strip()}
        except FileNotFoundError:
            trusted = set()
        
        return {"trusted": hostname in trusted}
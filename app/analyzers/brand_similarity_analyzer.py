from app.analyzers.base_analyzer import BaseAnalyzer
from typing import Dict, Any, List, Set


class BrandSimilarityAnalyzer(BaseAnalyzer):
    """Анализатор схожести с брендами на основе расстояния Левенштейна."""
    
    KNOWN_BRANDS = {
        "google", "paypal", "amazon", "apple", "microsoft", "facebook",
        "instagram", "telegram", "whatsapp", "discord", "steam", "binance",
        "openai", "twitter", "youtube", "github", "linkedin", "netflix",
        "gosuslugi", "sberbank", "tbank", "alfabank", "vtb", "yandex",
        "mail", "vk", "ozon", "wildberries", "avito", "icloud",
        "dropbox", "adobe", "stripe", "coinbase", "booking"
    }
    
    DISTANCE_RISK = {1: 50, 2: 35}
    BRAND_KEYWORD_RISK = 40
    HOSTNAME_BRAND_RISK = 40
    
    def analyze(self, url: str) -> Dict[str, Any]:
        self._reset()
        hostname = self._extract_hostname(url)
        
        if not hostname:
            return self._get_result()
        
        # Пропускаем IP-адреса
        if self._is_ip_address(hostname):
            return self._get_result()
        
        domain_name = self._extract_domain(hostname)
        if not domain_name:
            return self._get_result()
        
        mentioned_brands: Set[str] = set()
        
        # 1. Проверка на схожесть с брендами (расстояние Левенштейна)
        similar = self._find_similar_brands(domain_name)
        for brand, distance in similar:
            risk = self.DISTANCE_RISK.get(distance, 0)
            self._add_risk(risk, f"Ссылка имитирует бренд {brand.capitalize()}")
            mentioned_brands.add(brand)
        
        # 2. Проверка на упоминание бренда в домене
        brand_in_domain = self._find_brand_in_domain(domain_name)
        for brand in brand_in_domain:
            if brand not in mentioned_brands:
                self._add_risk(self.BRAND_KEYWORD_RISK, f"Ссылка использует бренд {brand.capitalize()}")
                mentioned_brands.add(brand)
        
        # 3. Проверка на упоминание бренда в поддомене
        brand_in_subdomain = self._find_brand_in_subdomain(hostname, domain_name)
        for brand in brand_in_subdomain:
            if brand not in mentioned_brands:
                self._add_risk(self.HOSTNAME_BRAND_RISK, f"Обнаружено упоминание бренда {brand.capitalize()} в поддомене")
                mentioned_brands.add(brand)
        
        return self._get_result()
    
    def _extract_domain(self, hostname: str) -> str:
        """Извлекает основное доменное имя (без TLD)."""
        labels = [label for label in hostname.split(".") if label]
        if len(labels) >= 2:
            return labels[-2]
        return labels[0] if labels else ""
    
    def _find_similar_brands(self, domain: str) -> List[tuple]:
        """Находит бренды, похожие на домен (по расстоянию Левенштейна)."""
        matches = []
        for brand in self.KNOWN_BRANDS:
            # Защита от ложных срабатываний
            if len(domain) < 5 or len(brand) < 5:
                continue
            
            distance = self._levenshtein(domain, brand)
            length_diff = abs(len(domain) - len(brand))
            
            if distance in self.DISTANCE_RISK and length_diff <= 2:
                matches.append((brand, distance))
        
        return matches
    
    def _find_brand_in_domain(self, domain: str) -> List[str]:
        """Находит бренды, упомянутые в домене."""
        matches = []
        for brand in self.KNOWN_BRANDS:
            if brand == domain:  # Настоящий домен бренда
                continue
            if brand in domain:
                matches.append(brand)
        return matches
    
    def _find_brand_in_subdomain(self, hostname: str, domain: str) -> List[str]:
        """Находит бренды, упомянутые в поддоменах."""
        labels = [label for label in hostname.split(".") if label]
        if len(labels) <= 2:
            return []
        
        subdomains = labels[:-2]
        matches = []
        for brand in self.KNOWN_BRANDS:
            if brand == domain:
                continue
            if any(brand in sub for sub in subdomains):
                matches.append(brand)
        return matches
    
    def _levenshtein(self, s1: str, s2: str) -> int:
        """Вычисляет расстояние Левенштейна между двумя строками."""
        if s1 == s2:
            return 0
        if not s1:
            return len(s2)
        if not s2:
            return len(s1)
        
        prev = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1, 1):
            curr = [i]
            for j, c2 in enumerate(s2, 1):
                insert = curr[j - 1] + 1
                delete = prev[j] + 1
                replace = prev[j - 1] + (c1 != c2)
                curr.append(min(insert, delete, replace))
            prev = curr
        
        return prev[-1]
    
    def _is_ip_address(self, hostname: str) -> bool:
        """Проверяет, является ли hostname IP-адресом."""
        try:
            from ipaddress import ip_address
            ip_address(hostname)
            return True
        except ValueError:
            return False
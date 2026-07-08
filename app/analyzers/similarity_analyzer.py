from app.analyzers.base_analyzer import BaseAnalyzer
from typing import Dict, Any, List, Tuple


class SimilarityAnalyzer(BaseAnalyzer):
    """Анализатор схожести домена с известными брендами."""
    
    # Константы
    LATIN_RANGES = ((0x0041, 0x005A), (0x0061, 0x007A))
    CYRILLIC_RANGES = ((0x0400, 0x04FF), (0x0500, 0x052F))
    GREEK_RANGES = ((0x0370, 0x03FF), (0x1F00, 0x1FFF))
    
    CHARACTER_SUBSTITUTIONS = {
        "0": "o", "@": "a", "3": "e", "5": "s", "1": "l", "9": "g"
    }
    
    MULTI_CHAR_SUBSTITUTIONS = {
        "rn": "m", "vv": "w", "cl": "d"
    }
    
    UNICODE_HOMOGLYPHS = {
        "а": "a", "е": "e", "о": "o", "р": "p", "с": "c",
        "у": "y", "х": "x", "і": "i", "ј": "j"
    }
    
    KNOWN_BRANDS = {
        "google", "paypal", "amazon", "apple", "microsoft", "facebook",
        "instagram", "telegram", "whatsapp", "discord", "steam", "binance",
        "openai", "twitter", "youtube", "github", "linkedin", "netflix",
        "gosuslugi", "sberbank", "tbank", "alfabank", "vtb", "yandex",
        "mail", "vk", "ozon", "wildberries", "avito", "icloud",
        "dropbox", "adobe", "stripe", "coinbase", "booking"
    }
    
    def analyze(self, url: str) -> Dict[str, Any]:
        self._reset()
        hostname = self._extract_hostname(url)
        
        if not hostname:
            return self._get_result()
        
        # Проверка на Punycode
        if any(label.startswith("xn--") for label in hostname.split(".")):
            self._add_risk(30, "Обнаружен домен в формате Punycode")
        
        # Проверка на смешанные алфавиты
        if self._has_mixed_scripts(hostname):
            self._add_risk(35, "Используются символы из разных алфавитов")
        
        # Проверка на подмену символов
        substitutions = self._get_detected_substitutions(hostname)
        if substitutions:
            self._add_risk(20, f"Подмена символа: {', '.join(substitutions)}")
        
        # Проверка на имитацию бренда
        impersonated = self._get_impersonated_brand(hostname)
        if impersonated:
            self._add_risk(50, f"Ссылка имитирует бренд {impersonated.capitalize()}")
        
        return self._get_result()
    
    def _has_mixed_scripts(self, hostname: str) -> bool:
        """Проверяет, используются ли символы из разных алфавитов."""
        scripts = set()
        for char in hostname:
            if self._is_latin(char):
                scripts.add("latin")
            elif self._is_cyrillic(char):
                scripts.add("cyrillic")
            elif self._is_greek(char):
                scripts.add("greek")
        return len(scripts) >= 2
    
    def _get_detected_substitutions(self, hostname: str) -> List[str]:
        """Возвращает список обнаруженных подмен символов."""
        detected = []
        
        for label in hostname.split("."):
            if not label:
                continue
            
            # Проверяем замены символов
            for sus, rep in self.CHARACTER_SUBSTITUTIONS.items():
                if sus in label:
                    normalized = label.replace(sus, rep)
                    if normalized in self.KNOWN_BRANDS:
                        detected.append(f"{sus} → {rep}")
            
            # Проверяем многобуквенные замены
            for sus, rep in self.MULTI_CHAR_SUBSTITUTIONS.items():
                if sus in label:
                    normalized = label.replace(sus, rep)
                    if normalized in self.KNOWN_BRANDS:
                        detected.append(f"{sus} → {rep}")
        
        return list(dict.fromkeys(detected))  # Уникальные
    
    def _get_impersonated_brand(self, hostname: str) -> str | None:
        """Определяет, какой бренд имитирует домен."""
        for brand in self.KNOWN_BRANDS:
            if brand in hostname:
                # Проверяем, что это не точное совпадение
                if hostname != brand:
                    return brand
        return None
    
    def _is_latin(self, char: str) -> bool:
        return self._is_in_ranges(char, self.LATIN_RANGES)
    
    def _is_cyrillic(self, char: str) -> bool:
        return self._is_in_ranges(char, self.CYRILLIC_RANGES)
    
    def _is_greek(self, char: str) -> bool:
        return self._is_in_ranges(char, self.GREEK_RANGES)
    
    @staticmethod
    def _is_in_ranges(char: str, ranges: Tuple[Tuple[int, int], ...]) -> bool:
        code = ord(char)
        return any(start <= code <= end for start, end in ranges)

#Что изменилось:
#   1. Функция → Класс
#   2. Все константы вынесены в класс (капсуляция)
#   3. Убраны дублирующиеся методы (_extract_hostname)
#   4.Логика разбита на отдельные методы
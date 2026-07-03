from ipaddress import ip_address
import re
from typing import TypedDict
from urllib.parse import ParseResult, unquote, urlparse


class StructureAnalysisResult(TypedDict):
    risk_score: int
    reasons: list[str]


SUSPICIOUS_TLDS = {
    ".xyz",
    ".top",
    ".click",
    ".shop",
    ".buzz",
    ".monster",
    ".zip",
    ".mov",
    ".cam",
    ".gq",
    ".cf",
    ".ml",
    ".tk",
    ".work",
    ".country",
    ".review",
}

URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "cutt.ly",
}

MAX_RISK_SCORE = 100


def analyze_structure(url: str) -> StructureAnalysisResult:
    risk_score = 0
    reasons: list[str] = []

    normalized_url = url.strip()
    parsed_url = _parse_url(normalized_url)
    hostname = _get_hostname(parsed_url)
    
    if _is_ip_address(hostname):
        return {
            "risk_score": 0,
            "reasons": [],
        }

    if _uses_explicit_http(normalized_url):
        risk_score += 15
        reasons.append("Используется HTTP вместо HTTPS")

    if len(normalized_url) > 75:
        risk_score += 10
        reasons.append("Ссылка слишком длинная")

    if hostname and len(hostname) > 40:
        risk_score += 10
        reasons.append("Домен слишком длинный")

    if _subdomain_count(hostname) >= 2:
        risk_score += 15
        reasons.append("Обнаружено много поддоменов")

    if hostname.count(".") >= 4:
        risk_score += 10
        reasons.append("Домен содержит слишком много точек")

    if hostname.count("-") >= 3:
        risk_score += 10
        reasons.append("Домен содержит много дефисов")

    if "--" in hostname:
        risk_score += 10
        reasons.append("Обнаружен двойной дефис")

    if _special_character_count(hostname) >= 3:
        risk_score += 10
        reasons.append("Обнаружено много специальных символов")

    if _digit_count(hostname) >= 5:
        risk_score += 10
        reasons.append("Домен содержит много цифр")

    if "@" in normalized_url:
        risk_score += 20
        reasons.append("Ссылка содержит символ @")

    #if _is_ip_address(hostname):
     #   risk_score += 20
      #  reasons.append("Вместо домена используется IP-адрес")

    if _is_local_or_private(hostname):
        risk_score += 25
        reasons.append("Ссылка указывает на локальный или приватный адрес")

    if _has_suspicious_tld(hostname):
        risk_score += 15
        reasons.append("Используется подозрительная доменная зона")

    if _has_nested_url(normalized_url):
        risk_score += 20
        reasons.append("Ссылка содержит вложенную ссылку")

    if _is_url_shortener(hostname):
        risk_score += 15
        reasons.append("Используется сервис сокращения ссылок")

    return {
        "risk_score": min(risk_score, MAX_RISK_SCORE),
        "reasons": reasons,
    }


def _parse_url(url: str) -> ParseResult:
    if "://" in url:
        return urlparse(url)

    return urlparse(f"//{url}")


def _get_hostname(parsed_url: ParseResult) -> str:
    try:
        hostname = parsed_url.hostname
    except ValueError:
        return ""

    return (hostname or "").rstrip(".").lower()


def _uses_explicit_http(url: str) -> bool:
    return url.lower().startswith("http://")


def _subdomain_count(hostname: str) -> int:
    if not hostname or _is_ip_address(hostname):
        return 0

    labels = [label for label in hostname.split(".") if label]
    return max(len(labels) - 2, 0)


def _digit_count(value: str) -> int:
    return sum(character.isdigit() for character in value)


def _special_character_count(hostname: str) -> int:
    special_characters = {"*", "_", "~", "="}
    return sum(character in special_characters for character in hostname)


def _is_ip_address(hostname: str) -> bool:
    if not hostname:
        return False

    try:
        ip_address(hostname)
    except ValueError:
        return False

    return True


def _is_local_or_private(hostname: str) -> bool:
    if hostname == "localhost":
        return True

    try:
        parsed_ip = ip_address(hostname)
    except ValueError:
        return False

    return parsed_ip.is_loopback or parsed_ip.is_private


def _has_suspicious_tld(hostname: str) -> bool:
    return any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS)


def _has_nested_url(url: str) -> bool:
    decoded_url = unquote(url).lower()
    search_start = 0

    if decoded_url.startswith("http://"):
        search_start = len("http://")
    elif decoded_url.startswith("https://"):
        search_start = len("https://")

    return re.search(r"https?://", decoded_url[search_start:]) is not None


def _is_url_shortener(hostname: str) -> bool:
    return any(
        hostname == shortener or hostname.endswith(f".{shortener}")
        for shortener in URL_SHORTENERS
    )

from socket import gaierror, gethostbyname
from typing import TypedDict
from urllib.parse import ParseResult, urlparse


class ReputationAnalysisResult(TypedDict):
    risk_score: int
    reasons: list[str]


MAX_RISK_SCORE = 100


def analyze_reputation(url: str) -> ReputationAnalysisResult:
    risk_score = 0
    reasons: list[str] = []

    hostname = _extract_hostname(url)

    if not hostname:
        return {
            "risk_score": 50,
            "reasons": [
                "Не удалось определить доменное имя"
            ],
        }

    if _has_dns_record(hostname):
        reasons.append(
            "DNS-запись домена найдена"
        )
    else:
        risk_score += 50
        reasons.append(
            "Домен не существует или не имеет DNS-записи"
        )

    return {
        "risk_score": min(risk_score, MAX_RISK_SCORE),
        "reasons": reasons,
    }


def _extract_hostname(url: str) -> str:
    parsed_url = _parse_url(url.strip())

    try:
        hostname = parsed_url.hostname
    except ValueError:
        return ""

    return (hostname or "").rstrip(".").lower()


def _parse_url(url: str) -> ParseResult:
    if "://" in url:
        return urlparse(url)

    return urlparse(f"//{url}")


def _has_dns_record(hostname: str) -> bool:
    try:
        gethostbyname(hostname)
        return True
    except gaierror:
        return False
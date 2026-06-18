from socket import gaierror, gethostbyname
from typing import TypedDict
from urllib.parse import ParseResult, urlparse
from datetime import datetime, timedelta

import requests


class ReputationAnalysisResult(TypedDict):
    risk_score: int
    reasons: list[str]


MAX_RISK_SCORE = 100

PHISHING_CACHE: set[str] = set()
LAST_CACHE_UPDATE: datetime | None = None

CACHE_LIFETIME = timedelta(hours=1)


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
            "Домен существует и доступен в интернете"
        )

    else:
        risk_score += 50
        reasons.append(
            "Домен не найден в интернете"
        )
    
    if _check_openphish(url):
        return {
            "risk_score": 100,
            "reasons": [
                "URL найден в базе известных фишинговых сайтов OpenPhish"
            ],
        }

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

def _check_openphish(url: str) -> bool:
    _update_openphish_cache()

    return url.strip() in PHISHING_CACHE

def _update_openphish_cache() -> None:
    global PHISHING_CACHE
    global LAST_CACHE_UPDATE

    if (
        LAST_CACHE_UPDATE is not None
        and datetime.now() - LAST_CACHE_UPDATE < CACHE_LIFETIME
    ):
        return

    try:
        response = requests.get(
            "https://openphish.com/feed.txt",
            timeout=10,
        )

        if response.status_code == 200:
            PHISHING_CACHE = set(
                response.text.splitlines()
            )

            LAST_CACHE_UPDATE = datetime.now()

            print(
                f"OpenPhish cache updated: "
                f"{len(PHISHING_CACHE)} URLs"
            )

    except requests.RequestException:
        pass
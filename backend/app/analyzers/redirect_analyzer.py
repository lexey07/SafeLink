from typing import TypedDict
from urllib.parse import urlparse

import requests


class RedirectAnalysisResult(TypedDict):
    risk_score: int
    reasons: list[str]


def analyze_redirects(url: str) -> RedirectAnalysisResult:
    try:
        normalized_url = (
            url if "://" in url
            else f"https://{url}"
        )

        response = requests.get(
            normalized_url,
            allow_redirects=True,
            timeout=5,
        )

        original_domain = (
            urlparse(normalized_url).hostname or ""
        )

        final_domain = (
            urlparse(response.url).hostname or ""
        )

        if (
            final_domain
            and original_domain
            and _normalize_domain(final_domain)
            != _normalize_domain(original_domain)
        ):
            return {
                "risk_score": 30,
                "reasons": [
                    (
                        "Обнаружен редирект на другой домен: "
                        f"{final_domain}"
                    )
                ],
            }

    except requests.RequestException:
        pass

    return {
        "risk_score": 0,
        "reasons": [],
    }

def _normalize_domain(domain: str) -> str:
    if domain.startswith("www."):
        return domain[4:]

    return domain
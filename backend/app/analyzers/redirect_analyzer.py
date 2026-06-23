from typing import TypedDict
from urllib.parse import urlparse

import requests


class RedirectAnalysisResult(TypedDict):
    risk_score: int
    reasons: list[str]


def analyze_redirects(
    response: requests.Response,
    original_url: str,
) -> RedirectAnalysisResult:

    try:
        normalized_url = (
            original_url
            if "://" in original_url
            else f"https://{original_url}"
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

    except Exception:
        pass

    return {
        "risk_score": 0,
        "reasons": [],
    }


def _normalize_domain(domain: str) -> str:
    if domain.startswith("www."):
        return domain[4:]

    return domain
from typing import TypedDict
from urllib.parse import urlparse
import ipaddress


class IPAnalysisResult(TypedDict):
    risk_score: int
    reasons: list[str]


def analyze_ip(url: str) -> IPAnalysisResult:
    try:
        normalized_url = (
            url if "://" in url
            else f"//{url}"
        )

        hostname = urlparse(normalized_url).hostname

        if not hostname:
            return {
                "risk_score": 0,
                "reasons": [],
            }

        ipaddress.ip_address(hostname)

        return {
            "risk_score": 30,
            "reasons": [
                "В ссылке используется IP-адрес вместо домена"
            ],
        }

    except ValueError:
        return {
            "risk_score": 0,
            "reasons": [],
        }
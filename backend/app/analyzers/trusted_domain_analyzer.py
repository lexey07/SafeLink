from typing import TypedDict
from urllib.parse import urlparse


class TrustedDomainResult(TypedDict):
    trusted: bool


def analyze_trusted_domain(url: str) -> TrustedDomainResult:
    hostname = _extract_hostname(url)

    try:
        with open(
            "app/trusted_domains.txt",
            "r",
            encoding="utf-8",
        ) as file:
            trusted_domains = {
                line.strip().lower()
                for line in file
                if line.strip()
            }

    except FileNotFoundError:
        trusted_domains = set()

    return {
        "trusted": hostname in trusted_domains
    }


def _extract_hostname(url: str) -> str:
    parsed = urlparse(
        url if "://" in url else f"//{url}"
    )

    return (parsed.hostname or "").lower()
from datetime import datetime
from typing import TypedDict
from urllib.parse import urlparse
from datetime import datetime, timezone


import whois


class DomainAgeAnalysisResult(TypedDict):
    risk_score: int
    reasons: list[str]


def analyze_domain_age(url: str) -> DomainAgeAnalysisResult:
    risk_score = 0
    reasons: list[str] = []

    try:
        parsed = urlparse(url)

        domain = parsed.hostname

        if not domain:
            domain = (
                url.replace("https://", "")
                .replace("http://", "")
                .split("/")[0]
            )

        from socket import gaierror, gethostbyname

        try:
            gethostbyname(domain)
        except gaierror:
            return {
                "risk_score": 0,
                "reasons": [],
            }

        domain_info = whois.whois(domain)

        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if not creation_date:
            return {
                "risk_score": 0,
                "reasons": [],
            }

        age_days = (
            datetime.now(timezone.utc) -
            creation_date.astimezone(timezone.utc)
        ).days

        if age_days < 30:
            risk_score += 40
            reasons.append(
                "Домен зарегистрирован менее месяца назад"
            )

        elif age_days < 180:
            risk_score += 25
            reasons.append(
                "Домен зарегистрирован менее 6 месяцев назад"
            )

        elif age_days < 365:
            risk_score += 10
            reasons.append(
                "Домен зарегистрирован менее года назад"
            )

        else:
            reasons.append(
                "Домен существует более года"
            )

    except Exception as error:
        print("WHOIS ERROR:", error)

        return {
            "risk_score": 0,
            "reasons": [],
        }

    return {
        "risk_score": risk_score,
        "reasons": reasons,
    }
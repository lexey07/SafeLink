from typing import TypedDict

import requests


class HtmlAnalysisResult(TypedDict):
    risk_score: int
    reasons: list[str]


def analyze_html(
    response: requests.Response,
) -> HtmlAnalysisResult:

    risk_score = 0
    reasons: list[str] = []

    try:
        html = response.text[:50000].lower()

        if 'type="password"' in html:
            risk_score += 15
            reasons.append(
                "На странице обнаружено поле ввода пароля"
            )

    except Exception:
        pass

    return {
        "risk_score": risk_score,
        "reasons": reasons,
    }
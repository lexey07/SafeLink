from typing import TypedDict

import requests


class HtmlAnalysisResult(TypedDict):
    risk_score: int
    reasons: list[str]


def analyze_html(url: str) -> HtmlAnalysisResult:
    risk_score = 0
    reasons: list[str] = []

    try:
        normalized_url = (
            url if "://" in url
            else f"https://{url}"
        )

        response = requests.get(
            normalized_url,
            timeout=5,
        )

        html = response.text.lower()

        if 'type="password"' in html:
            risk_score += 15
            reasons.append(
                "На странице обнаружено поле ввода пароля"
            )

        #if "<form" in html:
         #   risk_score += 10
          #  reasons.append(
           #     "На странице обнаружена форма ввода данных"
            #)

     #   suspicious_keywords = [
      #      "verify account",
       #     "confirm account",
        #    "update payment",
         #   "enter password",
          #  "login",
           # "sign in",
        #]

        #for keyword in suspicious_keywords:
         #   if keyword in html:
          #      risk_score += 5
           #     reasons.append(
            #        "Обнаружены признаки страницы авторизации"
             #   )
              #  break

    except requests.RequestException:
        pass

    return {
        "risk_score": risk_score,
        "reasons": reasons,
    }
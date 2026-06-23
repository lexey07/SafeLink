import requests


def explain_url(
    url: str,
    status: str,
    risk_score: int,
    reasons: list[str],
) -> str:

    prompt = f"""
Ты работаешь в антифишинговом сервисе SafeLink.

URL: {url}

Статус: {status}
Риск: {risk_score}/100

Причины:
{chr(10).join("- " + reason for reason in reasons)}

Объясни результат простым русским языком.

Правила:
- максимум 4 предложения
- без сложных терминов
- не перечисляй причины дословно
- если риск высокий, предупреди пользователя
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3:4b",
                "prompt": prompt,
                "stream": False,
            },
            timeout=30,
        )

        return response.json()["response"]

    except Exception as e:
        return f"ИИ временно недоступен: {str(e)}"
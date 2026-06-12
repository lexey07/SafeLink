from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def explain_url(url, status, risk_score, reasons):
    try:

        prompt = f"""
Проанализируй результат проверки ссылки.

URL: {url}

Статус: {status}

Риск: {risk_score}/100

Причины:
{chr(10).join(reasons)}

Объясни пользователю простым русским языком.
"""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"ИИ-анализ временно недоступен: {str(e)}"
from openai import OpenAI
from typing import List, Optional
from app.config import DEEPSEEK_API_KEY


class DeepSeekClient:
    """
    Клиент для работы с DeepSeek API.
    Инкапсулирует создание промптов, вызов API и обработку ошибок.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.deepseek.com",
        model: str = "deepseek-chat",
        temperature: float = 0.3,
        max_tokens: int = 300
    ):
        """
        Инициализация клиента DeepSeek.
        
        Args:
            api_key: API ключ DeepSeek
            base_url: Базовый URL API
            model: Модель для использования
            temperature: Температура генерации
            max_tokens: Максимальное количество токенов
        """
        self._api_key = api_key or DEEPSEEK_API_KEY
        self._client = OpenAI(
            api_key=self._api_key,
            base_url=base_url,
        )
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
    
    def explain_url(
        self,
        url: str,
        status: str,
        risk_score: int,
        reasons: List[str]
    ) -> str:
        """
        Получает объяснение результата проверки от DeepSeek.
        
        Args:
            url: Проверяемый URL
            status: Статус (Безопасно/Подозрительно/Высокий риск/Опасно)
            risk_score: Оценка риска (0-100)
            reasons: Список причин
        
        Returns:
            Объяснение от ИИ или fallback-ответ
        """
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": self._build_user_prompt(url, status, risk_score, reasons)}
                ],
                temperature=self._temperature,
                max_tokens=self._max_tokens,
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else self._get_fallback_response()
            
        except Exception as e:
            print(f"DeepSeek Error: {e}")
            return self._get_fallback_response()
    
    def _get_system_prompt(self) -> str:
        """Возвращает системный промпт."""
        return """Ты — ИИ-помощник сервиса SafeLink.

Твоя задача — объяснять результаты проверки ссылок, выполненной системой SafeLink.

ВАЖНЫЕ ПРАВИЛА:

1. Никогда не изменяй решение SafeLink.
2. Никогда не придумывай новые причины риска.
3. Используй только информацию, которую получил во входных данных.
4. Не делай предположений, которых нет в результатах анализа.
5. Пиши простым, понятным русским языком.
6. Не используй Markdown, эмодзи, смайлы и специальные символы.
7. Не здоровайся и не прощайся.
8. Не называй себя искусственным интеллектом.
9. Ответ должен состоять из 3–5 предложений.
10. Последним предложением всегда дай краткую рекомендацию пользователю.

Если ссылка безопасна — объясни почему.

Если ссылка подозрительная — объясни, какие признаки вызвали подозрение.

Если ссылка опасная — объясни, почему ей нельзя доверять.

Если информации недостаточно — прямо скажи об этом, не выдумывая дополнительные причины."""
    
    def _build_user_prompt(
        self,
        url: str,
        status: str,
        risk_score: int,
        reasons: List[str]
    ) -> str:
        """Собирает пользовательский промпт."""
        reasons_text = "\n".join(f"- {r}" for r in reasons) if reasons else "- Нет причин"
        
        return f"""SafeLink завершил анализ ссылки.

URL:
{url}

Статус:
{status}

Оценка риска:
{risk_score} из 100

Причины, обнаруженные анализаторами SafeLink:

{reasons_text}

Используя только эти данные:

1. Объясни пользователю, что означает результат проверки.
2. Простыми словами поясни каждую найденную причину.
3. Не добавляй причин, которых нет выше.
4. Не меняй оценку риска.
5. Закончи краткой рекомендацией."""
    
    def _get_fallback_response(self) -> str:
        """Возвращает fallback-ответ при ошибке."""
        return "Не удалось получить объяснение от ИИ. Результат проверки ссылки сформирован анализаторами SafeLink."


# ═══════════════════════════════════════════════════════════════
# ДЛЯ ОБРАТНОЙ СОВМЕСТИМОСТИ (чтобы старый код продолжал работать)
# ═══════════════════════════════════════════════════════════════

_client = DeepSeekClient()


def explain_url(
    url: str,
    status: str,
    risk_score: int,
    reasons: List[str]
) -> str:
    """
    Обратная совместимость со старым кодом.
    Вызывает метод explain_url у синглтона DeepSeekClient.
    """
    return _client.explain_url(url, status, risk_score, reasons)


def get_deepseek_client() -> DeepSeekClient:
    """Возвращает экземпляр DeepSeekClient для DI."""
    return _client

# Что изменилось:
#   1. Глобальный клиент → поле объекта
#   2. Функция → класс с методами
#   3. Промпты вынесены в отдельные методы
#   4. Обработка ошибок вынесена в отдельный метод
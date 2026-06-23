from typing import TypedDict


class AnalyzerResult(TypedDict):
    risk_score: int
    reasons: list[str]


class RiskEngineResult(TypedDict):
    status: str
    risk_score: int
    reasons: list[str]


MAX_RISK_SCORE = 100


def calculate_risk(*analyses: AnalyzerResult) -> RiskEngineResult:
    risk_score = min(_sum_risk_scores(analyses), MAX_RISK_SCORE)
    reasons = _deduplicate_and_sort_reasons(analyses)

    return {
        "status": _get_status(risk_score),
        "risk_score": risk_score,
        "reasons": reasons,
    }


def _sum_risk_scores(analyses: tuple[AnalyzerResult, ...]) -> int:

    return sum(
        analysis.get("risk_score", 0)
        for analysis in analyses
    )


def _deduplicate_and_sort_reasons(
    analyses: tuple[AnalyzerResult, ...],
) -> list[str]:

    unique_reasons = {
        reason
        for analysis in analyses
        for reason in analysis.get("reasons", [])
        if reason
    }

    critical_reasons = (
        "имитирует бренд",
        "Подмена символа",
        "OpenPhish",
        "IP-адрес",
        "Punycode",
        "алфавитов",
        "редирект",
    )

    has_critical_reason = any(
        any(keyword in reason for keyword in critical_reasons)
        for reason in unique_reasons
    )

    if has_critical_reason:
        unique_reasons = {
            reason
            for reason in unique_reasons
            if reason not in (
                "Домен существует более года",
                "Домен существует и доступен в интернете",
            )
        }

    def priority(reason: str) -> int:

        if "OpenPhish" in reason:
            return 0

        if "имитирует бренд" in reason:
            return 1

        if "Подмена символа" in reason:
            return 2

        if "алфавитов" in reason:
            return 3

        if "IP-адрес" in reason:
            return 4

        if "не найден" in reason:
            return 5

        return 100

    return sorted(
        unique_reasons,
        key=priority,
    )[:5]


def _get_status(risk_score: int):
    if risk_score == 0:
        return "Безопасно"

    if risk_score <= 30:
        return "Подозрительно"

    if risk_score <= 65:
        return "Высокий риск"

    return "Опасно"

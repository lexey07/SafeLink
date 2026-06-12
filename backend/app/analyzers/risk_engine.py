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
    return sum(analysis.get("risk_score", 0) for analysis in analyses)


def _deduplicate_and_sort_reasons(
    analyses: tuple[AnalyzerResult, ...],
) -> list[str]:
    unique_reasons = {
        reason
        for analysis in analyses
        for reason in analysis.get("reasons", [])
        if reason
    }

    return sorted(unique_reasons)


def _get_status(risk_score: int):
    if risk_score == 0:
        return "Безопасно"

    if risk_score <= 30:
        return "Подозрительно"

    if risk_score <= 65:
        return "Высокий риск"

    return "Опасно"

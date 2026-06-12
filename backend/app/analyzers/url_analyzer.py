from app.analyzers.structure_analyzer import analyze_structure
from app.analyzers.similarity_analyzer import analyze_similarity
from app.analyzers.brand_similarity_analyzer import (
    analyze_brand_similarity,
)
from app.analyzers.risk_engine import calculate_risk


def analyze_url(url: str):
    structure_result = analyze_structure(url)
    similarity_result = analyze_similarity(url)
    brand_result = analyze_brand_similarity(url)

    return calculate_risk(
        structure_result,
        similarity_result,
        brand_result,
    )

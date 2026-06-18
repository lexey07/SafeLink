from app.analyzers.structure_analyzer import analyze_structure
from app.analyzers.similarity_analyzer import analyze_similarity
from app.analyzers.brand_similarity_analyzer import (
    analyze_brand_similarity,
)
from app.analyzers.reputation_analyzer import (
    analyze_reputation,
)
from app.analyzers.risk_engine import calculate_risk
from app.analyzers.domain_age_analyzer import (
    analyze_domain_age,
)
from app.analyzers.trusted_domain_analyzer import (
    analyze_trusted_domain,
)
from app.analyzers.redirect_analyzer import (
    analyze_redirects,
)
from app.analyzers.html_analyzer import (
    analyze_html,
)
from app.analyzers.ip_analyzer import (
    analyze_ip,
)

def analyze_url(url: str):
    structure_result = analyze_structure(url)
    similarity_result = analyze_similarity(url)
    brand_result = analyze_brand_similarity(url)
    reputation_result = analyze_reputation(url)
    domain_age_result = analyze_domain_age(url)
    trusted_result = analyze_trusted_domain(url)
    redirect_result = analyze_redirects(url)
    html_result = analyze_html(url)
    ip_result = analyze_ip(url)

    if trusted_result["trusted"]:
        structure_result["risk_score"] = 0
        similarity_result["risk_score"] = 0
        brand_result["risk_score"] = 0

    return calculate_risk(
        structure_result,
        similarity_result,
        brand_result,
        reputation_result,
        domain_age_result,
        redirect_result,
        html_result,
        ip_result,
    )
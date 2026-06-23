from ipaddress import ip_address
from app.analyzers.structure_analyzer import analyze_structure
from app.analyzers.similarity_analyzer import analyze_similarity
import time
import requests
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

def _is_ip_address(url: str) -> bool:
    try:
        ip_address(url.strip())
        return True
    except ValueError:
        return False

def analyze_url(url: str):

    if _is_ip_address(url):
        reputation_result = analyze_reputation(url)
        ip_result = analyze_ip(url)

        return calculate_risk(
            reputation_result,
            ip_result,
        )

    structure_result = analyze_structure(url)
    start = time.time()
    structure_result = analyze_structure(url)
    print("STRUCTURE:", round(time.time() - start, 3))
    
    similarity_result = analyze_similarity(url)
    start = time.time()
    similarity_result = analyze_similarity(url)
    print("SIMILARITY:", round(time.time() - start, 3))
    
    brand_result = analyze_brand_similarity(url)
    start = time.time()
    brand_result = analyze_brand_similarity(url)
    print("BRAND:", round(time.time() - start, 3))

    reputation_result = analyze_reputation(url)
    start = time.time()
    reputation_result = analyze_reputation(url)
    print("REPUTATION:", round(time.time() - start, 3))

    domain_age_result = analyze_domain_age(url)
    start = time.time()
    domain_age_result = analyze_domain_age(url)
    print("DOMAIN_AGE:", round(time.time() - start, 3))

    trusted_result = analyze_trusted_domain(url)
    start = time.time()
    trusted_result = analyze_trusted_domain(url)
    print("TRUSTED:", round(time.time() - start, 3))

    response = None

    try:
        normalized_url = (
            url if "://" in url
            else f"https://{url}"
        )

        response = requests.get(
            normalized_url,
            allow_redirects=True,
            timeout=2,
        )

    except requests.RequestException:
        pass

    if response:
        redirect_result = analyze_redirects(
            response,
            url,
        )

        html_result = analyze_html(
            response,
        )

    else:
        redirect_result = {
            "risk_score": 0,
            "reasons": [],
        }

        html_result = {
            "risk_score": 0,
            "reasons": [],
        }

    ip_result = analyze_ip(url)
    start = time.time()
    ip_result = analyze_ip(url)
    print("IP:", round(time.time() - start, 3))

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
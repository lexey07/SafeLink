from typing import TypedDict
from urllib.parse import ParseResult, urlparse


class BrandSimilarityResult(TypedDict):
    risk_score: int
    reasons: list[str]


class SimilarBrandMatch(TypedDict):
    brand: str
    distance: int


class BrandKeywordMatch(TypedDict):
    brand: str


KNOWN_BRANDS = {
    "google",
    "paypal",
    "amazon",
    "apple",
    "microsoft",
    "facebook",
    "instagram",
    "telegram",
    "whatsapp",
    "discord",
    "steam",
    "binance",
    "openai",
    "twitter",
    "youtube",
    "github",
    "linkedin",
    "netflix",
    "gosuslugi",
    "sberbank",
    "tbank",
    "alfabank",
    "vtb",
    "yandex",
    "mail",
    "vk",
    "ozon",
    "wildberries",
    "avito",
    "icloud",
    "dropbox",
    "adobe",
    "stripe",
    "coinbase",
    "booking",
}

MAX_RISK_SCORE = 100
BRAND_KEYWORD_RISK_SCORE = 40
HOSTNAME_BRAND_RISK_SCORE = 40
DISTANCE_RISK_SCORES = {
    1: 50,
    2: 35,
}


def analyze_brand_similarity(url: str) -> BrandSimilarityResult:
    risk_score = 0
    reasons: list[str] = []

    hostname = _extract_hostname(url)
    domain_name = _extract_domain_name_without_tld(hostname)
    similar_brand_matches = _find_similar_brands(domain_name)
    brand_keyword_matches = _find_brand_keyword_matches(domain_name)
    hostname_brand_matches = _find_hostname_brand_matches(hostname, domain_name)
    brands_with_mention_reason: set[str] = set()

    if _is_ip_address(hostname):
        return {
            "risk_score": 0,
            "reasons": [],
        }

    for match in similar_brand_matches:
        brand = match["brand"]
        risk_score += DISTANCE_RISK_SCORES[match["distance"]]

        if brand not in brands_with_mention_reason:
            reasons.append(
                f"Ссылка имитирует бренд {_format_brand_name(brand)}"
            )
            brands_with_mention_reason.add(brand)

    for match in brand_keyword_matches:
        brand = match["brand"]
        risk_score += BRAND_KEYWORD_RISK_SCORE

        if brand not in brands_with_mention_reason:
            reasons.append(
                f"Ссылка использует бренд {_format_brand_name(brand)}"
            )
            brands_with_mention_reason.add(brand)

    for match in hostname_brand_matches:
        brand = match["brand"]
        risk_score += HOSTNAME_BRAND_RISK_SCORE

        if brand not in brands_with_mention_reason:
            reasons.append(
                "Обнаружено упоминание известного бренда в поддомене: "
                f"{_format_brand_name(brand)}"
            )
            brands_with_mention_reason.add(brand)

    return {
        "risk_score": min(risk_score, MAX_RISK_SCORE),
        "reasons": _deduplicate_reasons(reasons),
    }


def _extract_hostname(url: str) -> str:
    normalized_url = url.strip()
    parsed_url = _parse_url(normalized_url)

    try:
        hostname = parsed_url.hostname
    except ValueError:
        return ""

    return (hostname or "").rstrip(".").lower()


def _parse_url(url: str) -> ParseResult:
    if "://" in url:
        return urlparse(url)

    return urlparse(f"//{url}")


def _extract_domain_name_without_tld(hostname: str) -> str:
    labels = _hostname_labels(hostname)

    if len(labels) >= 2:
        return labels[-2]

    if labels:
        return labels[0]

    return ""


def _find_similar_brands(domain_name: str) -> list[SimilarBrandMatch]:
    if not domain_name:
        return []

    matches: list[SimilarBrandMatch] = []

    for brand in sorted(KNOWN_BRANDS):
        distance = _levenshtein_distance(domain_name, brand)

        # защита от ложных срабатываний
        if len(domain_name) < 5 or len(brand) < 5:
            continue

        length_difference = abs(
            len(domain_name) - len(brand)
        )

        if (
            distance in DISTANCE_RISK_SCORES
            and length_difference <= 2
        ):
            matches.append({
                "brand": brand,
                "distance": distance,
            })

    return matches


def _find_brand_keyword_matches(domain_name: str) -> list[BrandKeywordMatch]:
    if not domain_name:
        return []

    matches: list[BrandKeywordMatch] = []

    for brand in sorted(KNOWN_BRANDS):

        # настоящий домен бренда не должен получать риск
        if domain_name == brand:
            continue

        # ищем бренд внутри другого домена
        if brand in domain_name:
            matches.append({"brand": brand})

    return matches


def _find_hostname_brand_matches(
    hostname: str,
    domain_name: str,
) -> list[BrandKeywordMatch]:
    labels = _hostname_labels(hostname)

    if len(labels) <= 2:
        return []

    subdomain_labels = labels[:-2]
    matches: list[BrandKeywordMatch] = []

    for brand in sorted(KNOWN_BRANDS):
        if brand == domain_name:
            continue

        if any(brand in label for label in subdomain_labels):
            matches.append({"brand": brand})

    return matches


def _levenshtein_distance(first_value: str, second_value: str) -> int:
    if first_value == second_value:
        return 0

    if not first_value:
        return len(second_value)

    if not second_value:
        return len(first_value)

    previous_row = list(range(len(second_value) + 1))

    for first_index, first_character in enumerate(first_value, start=1):
        current_row = [first_index]

        for second_index, second_character in enumerate(second_value, start=1):
            insertion_cost = current_row[second_index - 1] + 1
            deletion_cost = previous_row[second_index] + 1
            substitution_cost = previous_row[second_index - 1]

            if first_character != second_character:
                substitution_cost += 1

            current_row.append(
                min(insertion_cost, deletion_cost, substitution_cost)
            )

        previous_row = current_row

    return previous_row[-1]


def _hostname_labels(hostname: str) -> list[str]:
    return [label for label in hostname.split(".") if label]


def _deduplicate_reasons(reasons: list[str]) -> list[str]:
    deduplicated_reasons: list[str] = []
    seen_reasons: set[str] = set()

    for reason in reasons:
        if reason in seen_reasons:
            continue

        deduplicated_reasons.append(reason)
        seen_reasons.add(reason)

    return deduplicated_reasons


def _format_brand_name(brand: str) -> str:
    return brand.capitalize()

from ipaddress import ip_address


def _is_ip_address(hostname: str) -> bool:
    try:
        ip_address(hostname)
        return True
    except ValueError:
        return False
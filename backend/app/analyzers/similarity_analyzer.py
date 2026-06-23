from typing import TypedDict
from urllib.parse import ParseResult, urlparse


class SimilarityAnalysisResult(TypedDict):
    risk_score: int
    reasons: list[str]


MAX_RISK_SCORE = 100

LATIN_RANGES = (
    (0x0041, 0x005A),
    (0x0061, 0x007A),
)

CYRILLIC_RANGES = (
    (0x0400, 0x04FF),
    (0x0500, 0x052F),
)

GREEK_RANGES = (
    (0x0370, 0x03FF),
    (0x1F00, 0x1FFF),
)

CHARACTER_SUBSTITUTIONS = {
    "0": "o",
    "@": "a",
    "3": "e",
    "5": "s",
    "1": "l",
    "9": "g",
}

HOSTNAME_NORMALIZATION_MAP = str.maketrans(CHARACTER_SUBSTITUTIONS)

MULTI_CHARACTER_SUBSTITUTIONS = {
    "rn": "m",
    "vv": "w",
    "cl": "d",
}

UNICODE_HOMOGLYPHS = {
    "а": "a",
    "е": "e",
    "о": "o",
    "р": "p",
    "с": "c",
    "у": "y",
    "х": "x",
    "і": "i",
    "ј": "j",
}

KNOWN_IMPERSONATION_TARGETS = {
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

    # РФ / СНГ
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

    # международные сервисы
    "icloud",
    "dropbox",
    "adobe",
    "stripe",
    "coinbase",
    "booking",
}


def analyze_similarity(url: str) -> SimilarityAnalysisResult:
    risk_score = 0
    reasons: list[str] = []

    hostname = _extract_hostname(url)
    possible_original_hostname = get_possible_original_hostname(hostname)
    unicode_normalized_hostname = (
        normalize_unicode_homoglyphs(
            possible_original_hostname
        )
    )
    fully_normalized_hostname = normalize_multichar_substitutions(
        possible_original_hostname
    )
    character_substitutions = _get_detected_character_substitutions(hostname)
    multichar_substitutions = _get_detected_multichar_substitutions(hostname)
    detected_substitutions = [
        *character_substitutions,
        *multichar_substitutions,
    ]
    impersonated_brand = _get_impersonated_brand(
        hostname,
        fully_normalized_hostname,
    )

    if _is_punycode_domain(hostname):
        risk_score += 30
        reasons.append("Обнаружен домен в формате Punycode")

    if _has_mixed_scripts(hostname):
        risk_score += 35
        reasons.append(
            "Используются символы из разных алфавитов"
        )

    if (
        unicode_normalized_hostname != possible_original_hostname
    ):
        risk_score += 40

    if possible_original_hostname != hostname and character_substitutions:
        risk_score += 20

        reasons.extend(
            f"Подмена символа: {substitution}"
            for substitution in character_substitutions
        )

    if multichar_substitutions:
        risk_score += 25
        reasons.extend(
            f"Подмена символа: {substitution}"
            for substitution in multichar_substitutions
        )

    if impersonated_brand:
        risk_score += 50
        reasons.append(
            f"Ссылка имитирует бренд {impersonated_brand.capitalize()}"
        )
    
    return {
        "risk_score": min(risk_score, MAX_RISK_SCORE),
        "reasons": reasons,
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


def normalize_hostname(hostname: str) -> str:
    return hostname.translate(HOSTNAME_NORMALIZATION_MAP)

def normalize_unicode_homoglyphs(
    hostname: str,
) -> str:
    normalized_hostname = hostname

    for fake_char, real_char in UNICODE_HOMOGLYPHS.items():
        normalized_hostname = normalized_hostname.replace(
            fake_char,
            real_char,
        )

    return normalized_hostname

def get_possible_original_hostname(hostname: str) -> str:

    labels = _hostname_labels(hostname)

    for label in labels:

        normalized_label = label

        for suspicious_value, replacement in CHARACTER_SUBSTITUTIONS.items():
            normalized_label = normalized_label.replace(
                suspicious_value,
                replacement,
            )

        if normalized_label in KNOWN_IMPERSONATION_TARGETS:
            return hostname.replace(label, normalized_label)

    return hostname


def normalize_multichar_substitutions(hostname: str) -> str:
    normalized_hostname = hostname

    for suspicious_value, replacement in MULTI_CHARACTER_SUBSTITUTIONS.items():
        normalized_hostname = normalized_hostname.replace(
            suspicious_value,
            replacement,
        )

    return normalized_hostname


def get_detected_substitutions(hostname: str) -> list[str]:
    return [
        *_get_detected_character_substitutions(hostname),
        *_get_detected_multichar_substitutions(hostname),
    ]


def _is_punycode_domain(hostname: str) -> bool:
    return any(label.startswith("xn--") for label in _hostname_labels(hostname))


def _has_mixed_scripts(hostname: str) -> bool:
    scripts = set()

    for character in hostname:
        if _is_latin(character):
            scripts.add("latin")
        elif _is_cyrillic(character):
            scripts.add("cyrillic")
        elif _is_greek(character):
            scripts.add("greek")

    return len(scripts) >= 2


def _get_detected_character_substitutions(hostname: str) -> list[str]:
    detected_substitutions: list[str] = []

    for label in _hostname_labels(hostname):

        normalized_label = label

        for suspicious_value, replacement in CHARACTER_SUBSTITUTIONS.items():
            normalized_label = normalized_label.replace(
                suspicious_value,
                replacement,
            )

        # проверяем только случаи,
        # когда после замены получился известный бренд
        if normalized_label in KNOWN_IMPERSONATION_TARGETS:

            for suspicious_value, replacement in CHARACTER_SUBSTITUTIONS.items():

                if suspicious_value in label:
                    detected_substitutions.append(
                        f"{suspicious_value} → {replacement}"
                    )

    return detected_substitutions


def _get_detected_multichar_substitutions(hostname: str) -> list[str]:
    detected_substitutions: list[str] = []

    for suspicious_value, replacement in MULTI_CHARACTER_SUBSTITUTIONS.items():
        if _has_meaningful_multichar_substitution(
            hostname,
            suspicious_value,
            replacement,
        ):
            detected_substitutions.append(f"{suspicious_value} → {replacement}")

    return detected_substitutions


def _has_meaningful_multichar_substitution(
    hostname: str,
    suspicious_value: str,
    replacement: str,
) -> bool:
    for label in _hostname_labels(hostname):
        if suspicious_value not in label:
            continue

        normalized_label = label.replace(suspicious_value, replacement)
        if normalized_label != label and _looks_like_known_target(label, normalized_label):
            return True

    return False


def _get_impersonated_brand(
    original_hostname: str,
    normalized_hostname: str,
) -> str | None:
    if normalized_hostname == original_hostname:
        return None

    for label in _hostname_labels(normalized_hostname):
        for brand in KNOWN_IMPERSONATION_TARGETS:
            if brand in label:
                return brand

    return None 


def _looks_like_known_target(original_label: str, normalized_label: str) -> bool:
    return any(
        target not in original_label and target in normalized_label
        for target in KNOWN_IMPERSONATION_TARGETS
    )


def _hostname_labels(hostname: str) -> list[str]:
    return [label for label in hostname.split(".") if label]


def _is_latin(character: str) -> bool:
    return _is_character_in_ranges(character, LATIN_RANGES)


def _is_cyrillic(character: str) -> bool:
    return _is_character_in_ranges(character, CYRILLIC_RANGES)


def _is_greek(character: str) -> bool:
    return _is_character_in_ranges(character, GREEK_RANGES)


def _is_character_in_ranges(
    character: str,
    ranges: tuple[tuple[int, int], ...],
) -> bool:
    codepoint = ord(character)
    return any(start <= codepoint <= end for start, end in ranges)

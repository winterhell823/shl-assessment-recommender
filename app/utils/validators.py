import re
from app.utils.constants import (
    COMPARISON_KEYWORDS,
    REFINEMENT_KEYWORDS,
    GREETING_KEYWORDS,
    TECH,
    ACCOUNTING,
    BANKING,
    CUSTOMER_SERVICE,
    SALES,
    MANAGEMENT
)

def normalize_text(text: str) -> str:
    if not text:
        return ""
    return text.lower().strip()

def is_comparison_query(query: str) -> bool:
    normalized = normalize_text(query)
    tokens = set(re.findall(r"[a-zA-Z0-9]+", normalized))
    return bool(tokens.intersection(COMPARISON_KEYWORDS) or any(kw in normalized for kw in ["vs", "versus"]))

def is_refinement_query(query: str, has_previous_recommendations: bool) -> bool:
    if not has_previous_recommendations:
        return False
    normalized = normalize_text(query)
    tokens = set(re.findall(r"[a-zA-Z0-9]+", normalized))
    return bool(tokens.intersection(REFINEMENT_KEYWORDS) or any(kw in normalized for kw in REFINEMENT_KEYWORDS))

def is_greeting(query: str) -> bool:
    normalized = normalize_text(query)
    greetings = [
        r"\bhi\b", r"\bhello\b", r"\bhey\b",
        r"\bgood\s+morning\b", r"\bgood\s+afternoon\b", r"\bgood\s+evening\b"
    ]
    if normalized in GREETING_KEYWORDS:
        return True
    return any(re.search(pattern, normalized) for pattern in greetings)

def contains_role_keywords(query: str) -> bool:
    normalized = normalize_text(query)
    tokens = set(re.findall(r"[a-zA-Z0-9]+", normalized))
    
    # Flat list of keywords
    all_role_words = set(TECH + ACCOUNTING + BANKING + CUSTOMER_SERVICE + SALES + MANAGEMENT)
    
    if tokens.intersection(all_role_words):
        return True
        
    # Multi-word checks
    multi_word_phrases = [
        "customer service", "customer support", "contact center",
        "call center", "chat support", "data analyst", "data scientist",
        "machine learning", "business development", "retail sales"
    ]
    return any(phrase in normalized for phrase in multi_word_phrases)

def extract_query_keywords(query: str) -> list[str]:
    normalized = normalize_text(query)
    tokens = re.findall(r"[a-zA-Z0-9]+", normalized)
    ignore_tokens = {
        "hiring", "hire", "need", "want", "assessment", "test",
        "candidate", "role", "looking", "for", "with",
        "and", "the", "a", "an", "to", "i", "we"
    }
    return [t for t in tokens if t not in ignore_tokens]

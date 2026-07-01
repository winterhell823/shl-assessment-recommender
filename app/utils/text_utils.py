import re


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", normalize_text(text))


def safe_join(values: list[str]) -> str:
    return " ".join(value for value in values if value)
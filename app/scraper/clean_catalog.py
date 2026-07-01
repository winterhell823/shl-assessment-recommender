import json
from pathlib import Path


RAW_PATH = Path("app/data/shl_catalog_raw.json")
CLEAN_PATH = Path("app/data/shl_catalog_clean.json")


def clean_catalog():
    if not RAW_PATH.exists():
        raise FileNotFoundError("Raw catalog file not found.")

    with open(RAW_PATH, "r", encoding="utf-8") as file:
        raw_items = json.load(file)

    clean_items = []

    for item in raw_items:
        name = item.get("name", "").strip()
        url = item.get("url", "").strip()

        if not name or not url:
            continue

        clean_items.append({
            "name": name,
            "url": url,
            "test_type": item.get("test_type", "").strip(),
            "description": item.get("description", "").strip(),
            "skills": item.get("skills", []),
            "keywords": item.get("keywords", [])
        })

    with open(CLEAN_PATH, "w", encoding="utf-8") as file:
        json.dump(clean_items, file, indent=2, ensure_ascii=False)

    return clean_items


if __name__ == "__main__":
    items = clean_catalog()
    print(f"Cleaned {len(items)} catalog items.")
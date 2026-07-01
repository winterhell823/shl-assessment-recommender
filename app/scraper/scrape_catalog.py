import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"
OUTPUT_PATH = Path("app/data/shl_catalog_raw.json")


def scrape_catalog():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(CATALOG_URL, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]
        name = link.get_text(strip=True)

        if not name:
            continue

        if "product-catalog" not in href:
            continue

        url = href if href.startswith("http") else BASE_URL + href

        item = {
            "name": name,
            "url": url,
            "test_type": "",
            "description": "",
            "skills": [],
            "keywords": []
        }

        items.append(item)

    unique_items = remove_duplicates(items)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(unique_items, file, indent=2, ensure_ascii=False)

    return unique_items


def remove_duplicates(items: list[dict]) -> list[dict]:
    seen = set()
    unique = []

    for item in items:
        url = item["url"]

        if url in seen:
            continue

        seen.add(url)
        unique.append(item)

    return unique


if __name__ == "__main__":
    data = scrape_catalog()
    print(f"Scraped {len(data)} catalog items.")
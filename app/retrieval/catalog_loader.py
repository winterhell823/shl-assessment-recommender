import json
from pathlib import Path


CATALOG_PATH = Path("app/data/shl_catalog_clean.json")


class CatalogLoader:
    def __init__(self, path: Path = CATALOG_PATH):
        self.path = path

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []

        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)
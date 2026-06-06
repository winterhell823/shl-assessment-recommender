from app.retrieval.catalog_loader import CatalogLoader


class RecommendationValidator:
    def __init__(self):
        self.catalog = CatalogLoader().load()
        self.valid_urls = {item.get("url") for item in self.catalog}

    def validate(self, recommendations: list[dict]) -> list[dict]:
        valid = []

        for rec in recommendations:
            if rec.get("url") in self.valid_urls:
                valid.append({
                    "name": rec.get("name"),
                    "url": rec.get("url"),
                    "test_type": rec.get("test_type")
                })

        return valid[:10]
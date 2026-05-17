import re
from app.retrieval.catalog_loader import CatalogLoader


class CatalogSearch:
    def __init__(self):
        self.catalog = CatalogLoader().load()
        # Ignore only ultra-generic tokens that add no value
        # Keep domain-specific terms: assessment, test, role, developer, skills, technical
        self.ignore_tokens = {
            "hiring", "hire", "need", "want",
            "candidate", "looking", "for", "with",
            "and", "the", "a", "an", "to", "please", "can", "could", "would", "should",
            "i", "you", "we", "they", "is", "are", "am", "be"
        }

    def search(self, query: str, limit: int = 20) -> list[dict]:
        # Filter out purely numeric pagination links or empty items
        filtered_catalog = []
        for item in self.catalog:
            name = item.get("name", "").strip()
            if not name or name.isdigit():
                continue
            
            # Standardize url/link field
            if "link" in item and "url" not in item:
                item["url"] = item["link"]
                
            filtered_catalog.append(item)

        query_tokens = self._tokenize(query)
        # Filter out generic/weak tokens
        filtered_tokens = [token for token in query_tokens if token not in self.ignore_tokens]

        if not filtered_tokens and query_tokens:
            filtered_tokens = query_tokens

        if not filtered_tokens:
            return []

        scored_items = []
        for item in filtered_catalog:
            score = 0
            name_lower = item.get("name", "").lower()
            desc_lower = item.get("description", "").lower()
            type_lower = item.get("test_type", "").lower()
            skills_lower = " ".join(item.get("skills", [])).lower()
            keywords_lower = " ".join(item.get("keywords", [])).lower()

            for token in filtered_tokens:
                # Direct exact boundary match in name gets highest priority
                if re.search(r'\b' + re.escape(token) + r'\b', name_lower):
                    score += 25
                elif token in name_lower:
                    score += 10
                
                # Match in test type
                if token in type_lower:
                    score += 5

                # Match in description
                if token in desc_lower:
                    score += 3
                    
                # Match in skills
                if re.search(r'\b' + re.escape(token) + r'\b', skills_lower):
                    score += 8
                elif token in skills_lower:
                    score += 4

                # Match in keywords
                if token in keywords_lower:
                    score += 3

            if score > 0:
                scored_items.append((score, item))

        # Sort by score descending
        scored_items.sort(key=lambda x: x[0], reverse=True)

        return [item for _, item in scored_items[:limit]]

    def find_by_name(self, name: str) -> dict | None:
        name_lower = name.lower()
        for item in self.catalog:
            if name_lower in item.get("name", "").lower():
                return item
        return None

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r"[a-zA-Z0-9]+", text.lower())
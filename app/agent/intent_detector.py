import re

class IntentDetector:
    def detect(self, text: str) -> str:
        text = text.lower().strip()

        # Detect greeting
        greetings = [
            r"\bhi\b", r"\bhello\b", r"\bhey\b",
            r"\bgood\s+morning\b", r"\bgood\s+afternoon\b", r"\bgood\s+evening\b"
        ]
        if any(re.search(pattern, text) for pattern in greetings):
            return "greeting"

        # Detect roles/skills indicating recommend intent
        recommend_keywords = [
            "recommend", "suggest", "hiring", "need", "assessment",
            "java", "python", "javascript", "react", "angular", "node",
            "backend", "frontend", "developer", "engineer", "software",
            "sql", "cloud", "aws", "devops", "qa", "tester", "automation",
            "machine learning", "data analyst", "data scientist",
            "accountant", "accounting", "accounts", "bookkeeping",
            "finance", "invoice", "bank", "banking", "branch",
            "teller", "cashier", "customer service", "customer support",
            "contact center", "call center", "chat support", "phone support",
            "sales", "business development", "retail sales",
            "manager", "leadership", "supervisor", "director"
        ]

        if any(word in text for word in recommend_keywords):
            return "recommend"

        if any(word in text for word in ["compare", "difference", "vs", "versus"]):
            return "compare"

        if any(word in text for word in ["actually", "change", "add", "remove", "instead"]):
            return "refine"

        return "unknown"
class Guardrails:
    BLOCKED_TOPICS = [
        "salary negotiation",
        "legal advice",
        "employment law",
        "contract law",
        "resume writing",
        "interview questions",
        "ignore previous instructions",
        "reveal prompt",
        "system prompt",
        "jailbreak"
    ]

    def is_out_of_scope(self, text: str) -> bool:
        text_lower = text.lower()

        for topic in self.BLOCKED_TOPICS:
            if topic in text_lower:
                return True

        return False
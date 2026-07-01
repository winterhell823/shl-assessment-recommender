from app.utils.validators import is_greeting, contains_role_keywords, normalize_text

class ContextExtractor:
    def get_latest_user_message(self, messages) -> str:
        for message in reversed(messages):
            if message.role == "user":
                return message.content
        return ""

    def get_conversation_text(self, messages) -> str:
        lines = []
        for message in messages:
            lines.append(f"{message.role}: {message.content}")
        return "\n".join(lines)

    def is_vague(self, text: str) -> bool:
        normalized = normalize_text(text)

        # 1. Greetings are NOT vague
        if is_greeting(normalized):
            return False

        # 2. Specific vague tech phrases
        vague_tech_phrases = [
            "software developer",
            "developer assessment",
            "technical test",
            "coding assessment",
            "software engineer",
            "programmer",
            "technical assessment",
            "coding test",
            "developer test",
            "i want test",
            "need test",
            "i need assessment"
        ]
        if any(phrase in normalized for phrase in vague_tech_phrases):
            return True

        # 3. Clear role/skill queries are NOT vague
        if contains_role_keywords(normalized):
            return False

        # 4. Generic queries are vague
        vague_phrases = [
            "i need an assessment",
            "suggest assessment",
            "recommend assessment"
        ]

        if any(phrase in normalized for phrase in vague_phrases):
            return True

        if len(normalized.split()) <= 4:
            return True

        return False
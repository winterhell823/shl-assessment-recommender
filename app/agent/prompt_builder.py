class PromptBuilder:
    def build_recommendation_prompt(
        self,
        conversation_text: str,
        catalog_items: list[dict]
    ) -> list[dict]:

        catalog_text = self._format_catalog(catalog_items)

        system_prompt = f"""
You are an SHL assessment recommendation assistant.

Rules:
- Only recommend assessments from the provided catalog.
- Do not invent assessment names or URLs.
- If the user is vague, ask one clear follow-up question.
- If the query is outside the SHL catalog or lacks enough detail, politely refuse and ask for more context.
- If enough context is available, recommend up to 15 assessments that are plausibly relevant.
- Keep the reply concise and recruiter-friendly.
- Stay focused only on SHL assessments.

Available catalog items:
{catalog_text}
"""

        user_prompt = f"""
Conversation:
{conversation_text}

Return a helpful assistant reply.
Do not output JSON.
"""

        return [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ]

    def _format_catalog(self, items: list[dict]) -> str:
        formatted = []

        for item in items:
            formatted.append(
                f"""
Name: {item.get("name")}
URL: {item.get("url")}
Test Type: {item.get("test_type")}
Description: {item.get("description")}
Skills: {", ".join(item.get("skills", []))}
""".strip()
            )

        return "\n\n".join(formatted)
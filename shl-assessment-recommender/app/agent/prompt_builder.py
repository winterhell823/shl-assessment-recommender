from app.prompts.recommendation_prompt import RECOMMENDATION_PROMPT
from app.prompts.comparison_prompt import COMPARISON_PROMPT
from app.prompts.refusal_prompt import REFUSAL_PROMPT

class PromptBuilder:
    def build_recommendation_prompt(self, conversation_text: str, catalog_items: list[dict]) -> str:
        items_str = self._format_items(catalog_items)
        return RECOMMENDATION_PROMPT.format(
            conversation_text=conversation_text,
            items_str=items_str
        ).strip()

    def build_comparison_prompt(self, conversation_text: str, catalog_items: list[dict]) -> str:
        items_str = self._format_items(catalog_items)
        return COMPARISON_PROMPT.format(
            conversation_text=conversation_text,
            items_str=items_str
        ).strip()

    def build_refusal_prompt(self, query: str, topic: str) -> str:
        return REFUSAL_PROMPT.format(
            query=query,
            topic=topic
        ).strip()

    def _format_items(self, catalog_items: list[dict]) -> str:
        items_str = ""
        for i, item in enumerate(catalog_items):
            items_str += f"{i+1}. Name: {item.get('name')}\n"
            items_str += f"   Type: {item.get('test_type')}\n"
            items_str += f"   Description: {item.get('description')}\n"
            items_str += f"   Skills: {', '.join(item.get('skills', []))}\n"
            items_str += f"   URL: {item.get('url') or item.get('link', '')}\n\n"
        return items_str.strip()

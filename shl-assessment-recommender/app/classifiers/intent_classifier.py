import re
from app.utils.constants import IntentType, OUT_OF_SCOPE_PATTERNS
from app.utils.validators import (
    is_comparison_query,
    is_refinement_query,
    is_greeting,
    contains_role_keywords,
    normalize_text
)
from app.utils.logger import get_logger

logger = get_logger("IntentClassifier")

class IntentClassifier:
    def detect_out_of_scope_topic(self, query: str) -> str | None:
        normalized = normalize_text(query)
        tokens = set(re.findall(r"[a-zA-Z0-9]+", normalized))

        for topic, patterns in OUT_OF_SCOPE_PATTERNS.items():
            for pattern in patterns:
                if " " in pattern:
                    if pattern in normalized:
                        logger.info(f"Out of scope match: '{pattern}' in topic '{topic}'")
                        return topic
                else:
                    if pattern in tokens:
                        logger.info(f"Out of scope token match: '{pattern}' in topic '{topic}'")
                        return topic
        return None

    def classify(self, query: str, has_previous_recommendations: bool = False) -> IntentType:
        # 1. Detect out-of-scope first
        out_of_scope_topic = self.detect_out_of_scope_topic(query)
        if out_of_scope_topic:
            logger.info(f"Query classified as REFUSE due to out-of-scope topic: {out_of_scope_topic}")
            return IntentType.REFUSE

        # 2. Detect comparison queries
        if is_comparison_query(query):
            logger.info("Query classified as COMPARE")
            return IntentType.COMPARE

        # 3. Detect refinement queries
        if is_refinement_query(query, has_previous_recommendations):
            logger.info("Query classified as REFINE")
            return IntentType.REFINE

        # 4. Detect greetings
        if is_greeting(query):
            logger.info("Query classified as GREETING")
            return IntentType.GREETING

        # 5. Detect role/skill-based recommendation queries
        if contains_role_keywords(query):
            logger.info("Query classified as RECOMMEND")
            return IntentType.RECOMMEND

        # 6. Otherwise clarify
        logger.info("Query classified as CLARIFY")
        return IntentType.CLARIFY

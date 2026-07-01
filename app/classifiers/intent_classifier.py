import re
from app.utils.constants import IntentType, OUT_OF_SCOPE_PATTERNS, RECOMMENDATION_ALLOWLIST
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

    def has_explicit_blocked_keywords(self, query: str) -> str | None:
        """Check for explicit blocked keywords that should ALWAYS refuse.
        
        Returns the blocked topic if found, None otherwise.
        
        These are more specific blocks that override the allowlist.
        """
        normalized = normalize_text(query)
        
        # Explicit blocks that override allowlist
        explicit_blocks = {
            "salary": ["salary", "compensation", "pay", "wage", "ctc", "offer amount"],
            "interviews": ["interview questions", "how to interview", "mock interview"],
            "legal": ["legal", "lawsuit", "attorney", "employment law"]
        }
        
        for topic, keywords in explicit_blocks.items():
            for keyword in keywords:
                if keyword in normalized:
                    logger.info(f"Query blocked by explicit keyword: '{keyword}' (topic: {topic})")
                    return topic
        
        return None

    def is_safe_recommendation_query(self, query: str) -> bool:
        """Check if query is in the safe recommendation allowlist.
        
        If query contains certain keywords, it's definitely a recommendation query
        and should NOT be blocked by out-of-scope checks.
        """
        normalized = normalize_text(query)
        tokens = set(re.findall(r"[a-zA-Z0-9]+", normalized))
        
        # Check if any allowlist word is in the query
        for allowlist_word in RECOMMENDATION_ALLOWLIST:
            if " " in allowlist_word:
                # Multi-word allowlist items
                if allowlist_word in normalized:
                    logger.info(f"Query marked as safe recommendation (allowlist match: '{allowlist_word}')")
                    return True
            else:
                # Single-word allowlist items
                if allowlist_word in tokens:
                    logger.info(f"Query marked as safe recommendation (allowlist token: '{allowlist_word}')")
                    return True
        
        return False

    def classify(self, query: str, has_previous_recommendations: bool = False) -> IntentType:
        # 1. Check for greetings first (lowest priority filter)
        if is_greeting(query):
            logger.info("Query classified as GREETING")
            return IntentType.GREETING

        # 2. Check for EXPLICIT blocked keywords (salary, interviews, legal) - BEFORE allowlist
        explicit_block = self.has_explicit_blocked_keywords(query)
        if explicit_block:
            logger.info(f"Query classified as REFUSE due to explicit blocked keyword (topic: {explicit_block})")
            return IntentType.REFUSE

        # 3. Check if it's a safe recommendation query (BEFORE out-of-scope checks)
        if self.is_safe_recommendation_query(query):
            logger.info("Query classified as RECOMMEND (safe allowlist match)")
            return IntentType.RECOMMEND

        # 4. Detect comparison queries
        if is_comparison_query(query):
            logger.info("Query classified as COMPARE")
            return IntentType.COMPARE

        # 5. Detect refinement queries
        if is_refinement_query(query, has_previous_recommendations):
            logger.info("Query classified as REFINE")
            return IntentType.REFINE

        # 6. Detect role/skill-based recommendation queries
        if contains_role_keywords(query):
            logger.info("Query classified as RECOMMEND")
            return IntentType.RECOMMEND

        # 7. NOW check for out-of-scope topics (AFTER recommendation checks)
        out_of_scope_topic = self.detect_out_of_scope_topic(query)
        if out_of_scope_topic:
            logger.info(f"Query classified as REFUSE due to out-of-scope topic: {out_of_scope_topic}")
            return IntentType.REFUSE

        # 8. Otherwise clarify
        logger.info("Query classified as CLARIFY")
        return IntentType.CLARIFY

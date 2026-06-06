from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from app.schemas import ChatRequest, ChatResponse, Recommendation
from app.agent.guardrails import Guardrails
from app.agent.context_extractor import ContextExtractor
from app.classifiers.intent_classifier import IntentClassifier
from app.agent.prompt_builder import PromptBuilder
from app.retrieval.search import CatalogSearch
from app.retrieval.vector_store import VectorStore
from app.retrieval.ranker import Ranker
from app.retrieval.relevance_filter import RelevanceFilter
from app.llm.llm_client import LLMClient
from app.utils.constants import IntentType
from app.utils.logger import get_logger

logger = get_logger("ChatAgent")

class ChatAgent:
    def __init__(self):
        self.guardrails = Guardrails()
        self.extractor = ContextExtractor()
        self.intent_classifier = IntentClassifier()
        self.search = None
        self.vector_store = None
        self.ranker = Ranker()
        self.relevance_filter = RelevanceFilter()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMClient()

    def _get_search(self) -> CatalogSearch:
        if self.search is None:
            self.search = CatalogSearch()
        return self.search

    def _get_vector_store(self) -> VectorStore:
        if self.vector_store is None:
            self.vector_store = VectorStore()
        return self.vector_store

    def handle_chat(self, request: ChatRequest) -> ChatResponse:
        latest_user_message = self.extractor.get_latest_user_message(request.messages)
        conversation_text = self.extractor.get_conversation_text(request.messages)

        # Base case scope/guardrail check
        if self.guardrails.is_out_of_scope(latest_user_message):
            return ChatResponse(
                reply="I can only help with SHL assessment recommendations and comparisons.",
                recommendations=[],
                end_of_conversation=False
            )

        # Determine has previous recommendations for refinement checks
        has_previous = False
        for msg in request.messages:
            if msg.role == "assistant" and "recommend" in msg.content.lower():
                has_previous = True
                break

        # 1. Intent Classification
        intent = self.intent_classifier.classify(latest_user_message, has_previous_recommendations=has_previous)
        logger.info(f"Detected query intent: {intent}")

        # 2. Refusal routing
        if intent == IntentType.REFUSE:
            topic = self.intent_classifier.detect_out_of_scope_topic(latest_user_message) or "General out-of-scope"
            try:
                refusal_prompt = self.prompt_builder.build_refusal_prompt(latest_user_message, topic)
                reply = self.llm.generate(refusal_prompt)
                if not reply or "LLM API key is missing" in reply:
                    raise ValueError("LLM generation failed")
            except Exception as e:
                logger.error(f"Refusal LLM generation failed: {e}")
                reply = f"I am unable to answer questions regarding {topic} as it is outside my scope. I am designed to assist with SHL assessment recommendations and comparisons. How can I help you find the right assessment?"
            
            return ChatResponse(
                reply=reply,
                recommendations=[],
                end_of_conversation=False
            )

        # 3. Greeting routing
        if intent == IntentType.GREETING:
            return ChatResponse(
                reply="Hi! I can help you find SHL assessments. What role or skills are you hiring for?",
                recommendations=[],
                end_of_conversation=False
            )

        # 4. Clarification routing
        if intent == IntentType.CLARIFY or self.extractor.is_vague(latest_user_message):
            vague_tech_keywords = {
                "developer", "programmer", "engineer", "coding", "software",
                "technical", "test", "assessment", "coder"
            }
            query_words = set(latest_user_message.lower().strip().split())
            if query_words.intersection(vague_tech_keywords):
                reply = "What programming language, framework, or technology stack should the assessment focus on?"
            else:
                reply = "Sure. What role are you hiring for, and what skills or seniority level should the assessment cover?"
                
            return ChatResponse(
                reply=reply,
                recommendations=[],
                end_of_conversation=False
            )

        # 5. Recommendation, Comparison, and Refinement routing
        query = latest_user_message if latest_user_message.strip() else conversation_text
        
        # Keyword search
        keyword_items = []
        try:
            keyword_items = self._get_search().search(query, limit=100)
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            keyword_items = []

        # Vector search with timeout fallback
        vector_items = []
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self._get_vector_store().search, query, 100)
                try:
                    vector_items = future.result(timeout=10)
                except FuturesTimeoutError as e:
                    future.cancel()
                    raise TimeoutError("Vector search took too long (10s)") from e

        except TimeoutError as e:
            logger.warning(f"Vector search timeout (using keyword search only): {e}")
            vector_items = []
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            vector_items = []

        # 6. Rank Results
        ranked_items = self.ranker.rank(keyword_items, vector_items, query)

        # 7. Category-Aware Relevance Filter
        filtered_items = self.relevance_filter.filter(latest_user_message, ranked_items)

        # 8. Safe Empty Handlers
        if not filtered_items:
            return ChatResponse(
                reply="I found some possible matches, but not a strong fit. Could you specify the role or main skills?",
                recommendations=[],
                end_of_conversation=False
            )

        # 9. Prompt selection and LLM generation
        if intent == IntentType.COMPARE:
            try:
                prompt = self.prompt_builder.build_comparison_prompt(
                    conversation_text=conversation_text,
                    catalog_items=filtered_items
                )
                reply = self.llm.generate(prompt)
                if not reply or "LLM API key is missing" in reply:
                    raise ValueError("LLM generation failed")
            except Exception as e:
                logger.error(f"LLM comparison generation failed: {e}")
                reply = "Here is a comparison of the top matching assessments based on measured skills and duration:"
        elif intent == IntentType.REFINE:
            try:
                prompt = self.prompt_builder.build_recommendation_prompt(
                    conversation_text=conversation_text,
                    catalog_items=filtered_items
                )
                reply = self.llm.generate(prompt)
                if not reply or "LLM API key is missing" in reply:
                    raise ValueError("LLM generation failed")
            except Exception as e:
                logger.error(f"LLM refinement generation failed: {e}")
                reply = "Based on your refined preferences, here are the updated recommendations:"
        else: # RECOMMEND or GENERAL_QUERY
            try:
                prompt = self.prompt_builder.build_recommendation_prompt(
                    conversation_text=conversation_text,
                    catalog_items=filtered_items
                )
                reply = self.llm.generate(prompt)
                if not reply or "LLM API key is missing" in reply:
                    raise ValueError("LLM generation failed")
            except Exception as e:
                logger.error(f"LLM recommendation generation failed: {e}")
                reply = "Based on your request, I recommend the following assessments from the SHL catalog to help evaluate candidates for this role:"

        # 10. Packaging final recommendations
        recommendations = []
        for item in filtered_items:
            rec_url = item.get("url") or item.get("link", "")
            recommendations.append(
                Recommendation(
                    name=item.get("name", "Assessment"),
                    url=rec_url,
                    test_type=item.get("test_type")
                )
            )

        return ChatResponse(
            reply=reply,
            recommendations=recommendations,
            end_of_conversation=False
        )
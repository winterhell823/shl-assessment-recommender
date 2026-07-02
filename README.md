# Live Demo 
 https://shl-assessment-recommender-3bw9-dc7mbplz6.vercel.app/ 
 
# SHL Assessment Recommender – Approach Summary

1. Problem Understanding

The objective was to build an AI-powered conversational assistant capable of recommending relevant SHL assessments based on hiring requirements while ensuring all recommendations remain grounded in the official SHL assessment catalog. The system needed to support clarification, recommendation, refinement, and comparison workflows while preventing hallucinations and out-of-scope responses.

Backend live link for testing : https://shl-assessment-recommender-9czk.onrender.com/docs#/default/chat_api_chat_post 

2. Design Choices
I adopted a Retrieval-Augmented Generation (RAG) architecture instead of relying solely on an LLM. Since recommendations must come exclusively from SHL catalog data, retrieval was treated as the source of truth and the LLM was used only for conversational reasoning and response generation.
Key design decisions:
Hybrid retrieval combining keyword matching and semantic search.
Catalog-first architecture to prevent hallucinated assessments.
Stateless FastAPI backend for scalability.
Modular pipeline separating retrieval, ranking, intent classification, and response generation.
Guardrails to enforce SHL-only responses.
3. Retrieval Setup
The SHL catalog was processed into structured documents containing:
Assessment name
Description
Assessment type
Skills measured
Job role relevance
SHL catalog URL
Sentence Transformers were used to generate embeddings for semantic search and stored in a FAISS index. At query time:
User query is analyzed.
Keyword retrieval identifies exact matches.
FAISS semantic retrieval finds conceptually similar assessments.
Results are combined and ranked.
Top relevant assessments are provided to the LLM as context.
This hybrid approach improved retrieval quality compared to either keyword or vector search alone.
4. Prompt Design
The system prompt strictly constrained the model to:
Use only retrieved catalog information.
Never invent assessments.
Never generate URLs not present in the catalog.
Ask clarifying questions when insufficient information is available.
Refuse unrelated, legal, hiring-advice, or prompt-injection requests.
The prompt also instructed the model to support:
Clarification
Recommendation
Refinement of existing recommendations
Assessment comparison
5. Evaluation Method
The system was evaluated using:
Recall@10 – Ability to retrieve relevant assessments.
Precision@10 – Quality of retrieved recommendations.
Groundedness Validation – Percentage of responses supported by catalog data.
Refusal Accuracy – Correct handling of out-of-scope and adversarial queries.
Retrieval Latency – Time required to retrieve recommendations.
Evaluation queries covered technical, cognitive, personality, and role-based hiring scenarios.
6. What Did Not Work
Several approaches produced suboptimal results:
Pure Keyword Search
Keyword-only retrieval missed semantically related terms.
Example:
"Banking Analyst"
"Finance Professional"
could retrieve different results despite similar intent.
Overly Aggressive Clarification
Early versions relied on rigid keyword rules and frequently asked unnecessary follow-up questions, reducing conversational quality and consuming available conversation turns.
Challenges
Resource Constraints: Optimized the system for a 512 MB RAM cloud deployment by persisting the FAISS index, reusing embeddings, and minimizing model loading.
Retrieval Quality: Improved recommendation relevance by combining keyword and semantic search into a hybrid retrieval pipeline.
Conversational Reliability: Reduced unnecessary clarifications, preserved conversation context, and ensured all recommendations remained grounded in the SHL catalog.







## Deployment
- Render
- Vercel

---

# Evaluation

- Recall@10
- Precision@10
- Groundedness Validation
- Exact Match Accuracy
- Refusal Accuracy

---

# Local Setup

## Install Dependencies

```bash
pip install -r requirements.txt
Add Environment Variables

Create .env:

GROQ_API_KEY=your_key
GROQ_MODEL=llama-3.1-8b-instant
Run Backend
uvicorn app.main:app --reload
API Endpoints
Health Check
GET /health
Chat Endpoint
POST /chat

Example:

{
  "messages": [
    {
      "role": "user",
      "content": "java developer"
    }
  ]
}
Notes
Recommendations are generated only from SHL catalog data.
LLM is used for conversational responses only.

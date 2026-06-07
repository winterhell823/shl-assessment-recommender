# Live Demo 
  https://shl-assessment-recommender-bor4.vercel.app/ 
# SHL Assessment Recommender

AI-powered conversational assistant for recommending relevant SHL assessments based on hiring requirements.

## Features

- SHL assessment recommendations
- Hybrid retrieval (Keyword + Vector Search)
- Intent classification
- Clarification handling
- Recommendation refinement
- Guardrails & refusal handling
- Grounded catalog-based responses

---

# Tech Stack

## Backend
- Python
- FastAPI
- Uvicorn

## AI / LLM
- Groq API
- Llama 3.1 8B Instant

## Retrieval
- FAISS
- Sentence Transformers
- Hybrid Search

## Frontend
- Next.js
- Tailwind CSS

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
Stateless API design used for scalability.

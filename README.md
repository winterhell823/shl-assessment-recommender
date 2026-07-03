# SHL Assessment Recommender

# Live Demo 
 https://shl-assessment-recommender-3bw9-dc7mbplz6.vercel.app/ 

 Backend live link for testing : https://shl-assessment-recommender-9czk.onrender.com/docs#/default/chat_api_chat_post  
 

An AI-powered conversational assistant that recommends relevant **SHL psychometric assessments** based on hiring requirements. The system combines **Hybrid Retrieval (Keyword + Semantic Search)** with **LLM-powered conversations** to deliver accurate, grounded, and context-aware assessment recommendations.

## 🚀 Features

- AI-powered conversational interface
- Hybrid Retrieval (Keyword + FAISS Vector Search)
- Semantic Search using Sentence Transformers
- Intent Classification & Clarification Handling
- Context-aware Recommendation Refinement
- Assessment Comparison
- Grounded, Catalog-Only Responses
- Prompt Injection & Out-of-Scope Guardrails
- Stateless REST API

---

## 🛠 Tech Stack

**Backend**
- Python
- FastAPI

**Frontend**
- Next.js
- Tailwind CSS

**AI / LLM**
- Groq API
- Llama 3.1 8B Instant

**Retrieval**
- FAISS
- Sentence Transformers
- Hybrid Search (Keyword + Vector Search)

**Deployment**
- Render
- Vercel

---

## 💡 Conversational Capabilities

### ✅ Clarification
Asks follow-up questions when hiring requirements are incomplete.

**Example**

**User:** I need an assessment.

**Assistant:** What role are you hiring for? Which skills or seniority level should the assessment evaluate?

---

### ✅ Recommendations
Returns **1–10 relevant SHL assessments** including:

- Assessment Name
- Brief Description
- Reason for Recommendation
- Official SHL Catalog URL

---

### ✅ Recommendation Refinement

The assistant updates recommendations when users modify their requirements instead of restarting the conversation.

**Example**

**User:** Recommend Java Developer assessments.

**User:** Also include personality assessments.

---

### ✅ Assessment Comparison

Supports grounded comparisons between SHL assessments using only catalog information.

**Example**

> Compare OPQ and GSA.

---

## 🛡 Guardrails

The assistant only responds to queries related to SHL assessments and refuses:

- General hiring advice
- Legal questions
- Prompt injection attempts
- Requests outside the SHL assessment catalog

All recommendations and URLs are generated exclusively from the official SHL catalog.

---

## ⚙️ Local Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create `.env`

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

### Run Backend

```bash
uvicorn app.main:app --reload
```

### Run Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📡 API Endpoints

### Health Check

```http
GET /health
```

### Chat

```http
POST /chat
```

Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Recommend assessments for a Java Backend Developer with Spring Boot experience."
    }
  ]
}
```

---

## 📊 Evaluation

The system was evaluated using:

- Recall@10
- Precision@10
- Groundedness Validation
- Refusal Accuracy

These metrics assess retrieval quality, recommendation relevance, response grounding, and safe handling of out-of-scope requests.

---

## ⚠️ Challenges

- Optimized deployment for a **512 MB RAM** cloud environment by persisting the FAISS index and reusing embeddings.
- Improved recommendation quality through **hybrid retrieval** combining keyword and semantic search.
- Reduced unnecessary clarifications while maintaining grounded multi-turn conversations.

---

## 🔮 Future Improvements

- Cross-Encoder Re-ranking
- Larger Embedding Models
- Metadata-aware Retrieval
- Long-term Conversation Memory
- Streaming Responses
- Response Caching

---

## 👨‍💻 Author

**Vaibhav Sharma**

Engineering Student | AI & Software Developer

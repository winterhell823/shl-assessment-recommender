from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.routes import router as chat_router
from app.config import settings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for SHL Assessment Recommender"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, this should be the specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(chat_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "SHL Assessment Recommender API is running",
        "health": "/health",
        "chat": "/chat"
    }
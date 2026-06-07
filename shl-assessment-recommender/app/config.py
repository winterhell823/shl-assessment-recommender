from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SHL Assessment Recommender"
    app_version: str = "1.0.0"

    groq_api_key: str | None = None
    groq_model: str = "llama-3.1-8b-instant"

    catalog_path: str = "app/data/shl_catalog_clean.json"
    max_recommendations: int = 10
    enable_vector_search: bool = False
    vector_search_timeout_seconds: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
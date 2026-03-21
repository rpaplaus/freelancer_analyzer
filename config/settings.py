from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Freelancer Analyzer"
    VERSION: str = "1.0.0"

    # PostgreSQL Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/freelancer_db"

    # External APIs
    OPENAI_API_KEY: str | None = None
    APIFY_API_KEY: str | None = None
    APIFY_USER_ID: str | None = None
    APIFY_ACTOR_ID: str = "jupri/upwork-scraper"
    
    # Scheduling Intervals (minutes)
    SCRAPE_INTERVAL_MINUTES: int = 15
    STATS_INTERVAL_MINUTES: int = 30
    SCORING_INTERVAL_MINUTES: int = 30
    LLM_INTERVAL_MINUTES: int = 60
    
    # Vector DB Directory (Chroma DB)
    CHROMA_PERSIST_DIR: str = "./chroma_db"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()

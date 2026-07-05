from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    database_url: str
    daily_kcal_goal: int = 2200

    class Config:
        env_file = ".env"

settings = Settings()
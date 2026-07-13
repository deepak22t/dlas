from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
    env_file=".env"
)   
    postgres_user: str = "username"
    postgres_password: str = "password"
    postgres_db: str = "dlas_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    redis_password: str = "redis_password"
    redis_port: int = 6379
    redis_host: str = "localhost"
    redis_db: int = 0
    
    llm_provider: str = "groq"    
    groq_api_key: str
    groq_model: str

    @property
    def redis_url(self) -> str:
        return (
            f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
        )
        
    @property
    def database_url(self) -> str:
        return (
            f"postgresql://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    app_name: str = "DLAS Backend"
    debug: bool = True

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


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
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    app_name: str = "DLAS Backend"
    debug: bool = True

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


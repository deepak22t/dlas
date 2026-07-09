from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
    env_file=".env"
)
    app_name: str = "DLAS Backend"
    debug: bool = True

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


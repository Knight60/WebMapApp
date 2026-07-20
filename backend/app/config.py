from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Earth Engine service account
    ee_service_account_email: str = ""
    ee_private_key_path: str = ""
    ee_private_key_json: str = ""
    gcp_project_id: str = ""

    # CORS
    allowed_origins: list[str] = ["http://localhost:5173"]

    # Composite behavior
    target_year: int = 2026
    current_date_override: str = ""  # e.g. "2026-07-20", empty = use real today


@lru_cache
def get_settings() -> Settings:
    return Settings()

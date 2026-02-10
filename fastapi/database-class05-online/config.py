from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    database_url: str = ""
    secret_key: str = ""  # For signing tokens
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()

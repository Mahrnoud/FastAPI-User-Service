from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    USE_DB_REPLICATION: bool = False

    # Default database
    DATABASE_URL: str = None

    # Master/slave setup (used if USE_DB_REPLICATION is true)
    DATABASE_WRITE_URL: str = None
    DATABASE_READ_URL: str = None

    # JWT and other configs
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Email settings
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str

    # Default language for translations
    DEFAULT_LANGUAGE: str = "en"

    class Config:
        env_file = ".env"


settings = Settings()

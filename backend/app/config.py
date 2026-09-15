from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ACCESS_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_EXPIRE_DAYS: int = 30
    FERNET_KEY: str
    PLAID_CLIENT_ID: str
    PLAID_SECRET: str
    PLAID_ENV: str  # sandbox | development | production
    SSL_CERT_PATH: str
    SSL_KEY_PATH: str
    CORS_ALLOWED_ORIGIN: str = ""
    RATE_LIMIT_LOGIN_ATTEMPTS: int = 5
    RATE_LIMIT_WINDOW_MINUTES: int = 5
    ENV: str = "development"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

# TODO: fail loudly at startup if PLAID_ENV doesn't match PLAID_CLIENT_ID/SECRET
# (e.g. sandbox keys used with PLAID_ENV=production) -- known footgun, see plan checklist.

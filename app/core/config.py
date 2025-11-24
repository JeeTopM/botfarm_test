from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Botfarm"
    API_V1_PREFIX: str = "/api/v1"

    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "botfarm"
    POSTGRES_USER: str = "botfarm"
    POSTGRES_PASSWORD: str = "botfarm"

    class Config:
        env_file = ".env"


settings = Settings()

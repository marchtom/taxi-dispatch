from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # TODO: use pydantic's SecretStr
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

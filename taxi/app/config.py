from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dispatch_url: AnyHttpUrl

    # Taxi movement
    speed_min: int = 1
    speed_max: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

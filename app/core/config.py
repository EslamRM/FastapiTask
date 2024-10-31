import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/demodb")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "demodb")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    @property
    def REDIS_URL(self):
        # Construct the Redis URL
        return f"redis://{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"


settings = Settings()

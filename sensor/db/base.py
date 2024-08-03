from pydantic_settings import BaseSettings
from redis.asyncio import Redis, ConnectionPool
import aioredis


class Settings(BaseSettings):
    redis_host: str = '127.0.0.1'
    redis_port: int = 6379
    redis_db: int = 0


settings = Settings()
pool = aioredis.ConnectionPool.from_url(f'redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}', max_connections=20)


def get_session():
    session = aioredis.Redis(connection_pool=pool)
    yield session
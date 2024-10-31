from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from app.core.config import settings

# MongoDB connection setup
class MongoDB:
    client: AsyncIOMotorClient = None # type: ignore

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(settings.MONGODB_URI)
    print("Connected to MongoDB")

async def close_mongo_connection():
    mongodb.client.close()
    print("Closed MongoDB connection")

async def get_mongo_database():
    if not mongodb.client:
        await connect_to_mongo()
    return mongodb.client["demodb"]

# Redis connection setup
class RedisDB:
    client: Redis = None

redisdb = RedisDB()

async def connect_to_redis():
    redisdb.client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )
    await redisdb.client.ping()
    print("Connected to Redis")

async def close_redis_connection():
    await redisdb.client.close()
    print("Closed Redis connection")

from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import UserInDB
from app.schemas.auth import UserCreate
from bson import ObjectId
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user: UserCreate, database: AsyncIOMotorClient) -> UserInDB:
    hashed_password = pwd_context.hash(user.password)
    user_data = UserInDB(name=user.name, email=user.email, hashed_password=hashed_password)
    await database["users"].insert_one(user_data.dict())
    return user_data


async def get_user_by_email(email: str, database: AsyncIOMotorClient) -> UserInDB:
    user = await database["users"].find_one({"email": email})
    return UserInDB(**user) if user else None


async def update_user(
    user_id: str, user_data: UserCreate, database: AsyncIOMotorClient
) -> UserInDB:
    hashed_password = pwd_context.hash(user_data.password)
    await database["users"].update_one(
        {"_id": ObjectId(user_id)}, {"$set": {"hashed_password": hashed_password}}
    )
    updated_user = await database["users"].find_one({"_id": ObjectId(user_id)})
    return UserInDB(**updated_user) if updated_user else None


async def delete_user(user_id: str, database: AsyncIOMotorClient) -> None:
    await database["users"].delete_one({"_id": ObjectId(user_id)})

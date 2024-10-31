from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.user import get_user_by_email

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str, database: AsyncIOMotorClient):
    user = await get_user_by_email(email, database)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None

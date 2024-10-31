import logging
from datetime import timedelta
from app.core.config import settings
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_mongo_database
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas.auth import UserCreateResponse, UserCreate, UserLogin, Token
from app.services.user import (
    create_user,
)
from app.core.security import (
    create_jwt_token as create_access_token,
    authenticate_user,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/signup", response_model=UserCreateResponse)
async def signup(
    user_data: UserCreate, database: AsyncIOMotorClient = Depends(get_mongo_database)
):
    logger.info("Attempting to create a user with data: %s", user_data)
    user = await create_user(user_data, database)

    if not user:
        logger.error("User creation failed for data: %s", user_data)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed"
        )

    logger.info("User created successfully: %s", user)
    return {"message": "User created successfully"}


@router.post("/signin", response_model=Token)
async def signin(
    user_data: UserLogin, database: AsyncIOMotorClient = Depends(get_mongo_database)
):
    user = await authenticate_user(user_data.email, user_data.password, database)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_access_token(
        data={"email": user_data.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_access_token(
        data={"email": user.email}, expires_delta=refresh_token_expires
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "message": "Welcome back!",
    }

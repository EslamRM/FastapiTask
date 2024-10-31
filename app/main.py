from fastapi import FastAPI
from app.routers import auth, organization, revoke_token
from app.core.database import connect_to_mongo, close_mongo_connection, connect_to_redis, close_redis_connection

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(organization.router, prefix="/organization", tags=["Organization"])
app.include_router(revoke_token.router, prefix="/auth", tags=["Token Revocation"])

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    await connect_to_redis()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
    await close_redis_connection()

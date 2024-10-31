from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    message: str


class TokenData(BaseModel):
    email: str


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenRevokeRequest(BaseModel):
    refresh_token: str

class UserCreateResponse(BaseModel):
    message: str
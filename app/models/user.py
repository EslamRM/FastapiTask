from bson import ObjectId
from pydantic.v1 import BaseModel, EmailStr, Field
from typing import Optional, ClassVar


# Custom ObjectId type for MongoDB compatibility with Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        return {"type": "string"}


# User model as stored in the database
class UserInDB(BaseModel):
    constant_value: ClassVar[str] = "constant"
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True

    class Config:
        populate_by_name = True  # Updated from `allow_population_by_field_name`
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


# Schema for user creation
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# Schema for user response
class UserResponse(BaseModel):
    id: PyObjectId
    name: str
    email: EmailStr

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

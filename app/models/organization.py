from pydantic.v1 import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List


# Custom ObjectId field for MongoDB compatibility with Pydantic
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
    def __get_pydantic_json_schema__(cls, *args, **kwargs):
        return {"type": "string"}


# Define organization member structure
class OrganizationMember(BaseModel):
    email: EmailStr  # Use colon for type annotation
    access_level: str  # E.g., "read-only" or "admin"


# Define main organization model as stored in MongoDB
class OrganizationInDB(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    members: List[OrganizationMember] = (
        []
    )

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

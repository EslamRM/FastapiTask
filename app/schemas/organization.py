from pydantic import BaseModel
from typing import List, Optional


class OrganizationCreate(BaseModel):
    name: str
    description: str

class OrganizationCreateResponse(BaseModel):
    organization_id: str

class OrganizationUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class OrganizationResponse(BaseModel):
    organization_id: str
    name: str
    description: str
    organization_members: Optional[List[dict]] = []


class UserInvitation(BaseModel):
    user_email: str

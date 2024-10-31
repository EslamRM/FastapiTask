from motor.motor_asyncio import AsyncIOMotorClient
from app.models.organization import OrganizationInDB, OrganizationMember
from app.schemas.organization import OrganizationCreate
from fastapi import HTTPException, status
from bson import ObjectId
from typing import List, Dict
from .user import get_user_by_email


async def get_organization_by_name(
    name: str, database: AsyncIOMotorClient
) -> OrganizationInDB:
    organization = await database["organizations"].find_one({"name": name})
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    return OrganizationInDB(**organization)


async def create_organization(
    org_data: OrganizationCreate, current_user: dict, database: AsyncIOMotorClient
) -> dict:
    user = await get_user_by_email(current_user["email"], database)
    organization = OrganizationInDB(
        name=org_data.name,
        description=org_data.description,
        members=[
            {"name": user.name, "email": current_user["email"], "access_level": "owner"}
        ],
    )

    result = await database["organizations"].insert_one(organization.dict())

    return {
        "organization_id": str(result.inserted_id),
    }


async def get_organization(
    org_id: str, database: AsyncIOMotorClient
) -> OrganizationInDB:
    organization = await database["organizations"].find_one({"_id": ObjectId(org_id)})
    return OrganizationInDB(**organization) if organization else None


async def update_organization(
    org_id: str, org_data: OrganizationCreate, database: AsyncIOMotorClient
) -> OrganizationInDB:
    await database["organizations"].update_one(
        {"_id": ObjectId(org_id)}, {"$set": org_data.dict()}
    )
    updated_org = await database["organizations"].find_one({"_id": ObjectId(org_id)})
    return OrganizationInDB(**updated_org) if updated_org else None


async def delete_organization(org_id: str, database: AsyncIOMotorClient) -> None:
    await database["organizations"].delete_one({"_id": ObjectId(org_id)})


async def get_all_organizations(user, database: AsyncIOMotorClient) -> List[Dict]:
    cursor = database["organizations"].find(
        {"members": {"$elemMatch": {"email": user["email"]}}}
    )
    organizations = await cursor.to_list(length=100)
    formatted_organizations = []
    for org in organizations:
        formatted_org = {
            "organization_id": str(org["_id"]),
            "name": org.get("name", ""),
            "description": org.get("description", ""),
            "organization_members": [
                {
                    "name": member.get("name", ""),
                    "email": member.get("email", ""),
                    "access_level": member.get("access_level", ""),
                }
                for member in org.get("members", [])
            ],
        }
        formatted_organizations.append(formatted_org)

    return formatted_organizations


async def invite_user(organization_id, user_email, database: AsyncIOMotorClient):
    # Check if the inviting user is a member and has permission to invite
    organization = await database["organizations"].find_one(
        {"_id": ObjectId(organization_id)}
    )
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        )

    # Check if the user is already invited
    if any(member["email"] == user_email for member in organization["members"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of the organization",
        )

    # Add the new user to the members list with read-only access
    await database["organizations"].update_one(
        {"_id": ObjectId(organization_id)},
        {"$push": {"members": {"email": user_email, "access_level": "read-only"}}},
    )

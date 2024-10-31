from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.database import get_mongo_database
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationCreateResponse,
    OrganizationUpdate,
    OrganizationResponse,
    UserInvitation,
)
from app.services.organization import (
    create_organization,
    get_organization,
    get_all_organizations,
    update_organization,
    delete_organization,
    invite_user,
)
from app.core.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=OrganizationCreateResponse)
async def create_organization_route(
    org_data: OrganizationCreate,
    user: dict = Depends(get_current_user),
    database: AsyncIOMotorClient = Depends(get_mongo_database),
):
    return await create_organization(org_data, user, database)


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def read_organization(
    organization_id: str,
    database: AsyncIOMotorClient = Depends(get_mongo_database),
):
    organization = await get_organization(organization_id, database)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        )
    return OrganizationResponse(
        organization_id=str(organization.id),  # Ensure this is passed correctly
        name=organization.name,
        description=organization.description,
        members=organization.members,  # Adjust according to your data structure
    )


@router.get("/", response_model=list[OrganizationResponse])
async def read_all_organizations(
    user: dict = Depends(get_current_user),
    database: AsyncIOMotorClient = Depends(get_mongo_database),
):
    return await get_all_organizations(user, database)


@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization_route(
    organization_id: str,
    org_data: OrganizationUpdate,
    database: AsyncIOMotorClient = Depends(get_mongo_database),
):
    updated_organization = await update_organization(
        organization_id, org_data, database
    )
    if not updated_organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        )
    return OrganizationResponse(
        organization_id=str(updated_organization.id),  # Ensure this is passed correctly
        name=updated_organization.name,
        description=updated_organization.description,
        members=updated_organization.members,  # Adjust according to your data structure
    )


@router.delete("/{organization_id}")
async def delete_organization_route(
    organization_id: str,
    database: AsyncIOMotorClient = Depends(get_mongo_database),
):
    await delete_organization(organization_id, database)
    return {"message": "Organization deleted successfully"}


@router.post("/{organization_id}/invite")
async def invite_user_to_organization(
    organization_id: str,
    invitation: UserInvitation,
    database: AsyncIOMotorClient = Depends(get_mongo_database),
):
    await invite_user(organization_id, invitation.user_email, database)
    return {"message": "User invited successfully"}

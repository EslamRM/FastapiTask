import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.main import app

BASE_URL = "http://localhost:8080"

@pytest_asyncio.fixture(autouse=True)
async def async_client():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        yield client

@pytest.mark.asyncio
async def test_create_and_read_organization(async_client):
    # Sign in to get an access token
    signin_response = await async_client.post("/auth/signin", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    
    # Check if the sign-in was successful
    assert signin_response.status_code == 200
    access_token = signin_response.json().get("access_token")
    assert access_token is not None, "Access token should not be None"
    
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create an organization
    create_response = await async_client.post("/organization", json={
        "name": "Test Organization",
        "description": "An organization for testing purposes."
    }, headers=headers)
    
    assert create_response.status_code == 201
    response_data = create_response.json()
    assert "organization_id" in response_data
    organization_id = response_data["organization_id"]

    # Read the created organization
    read_response = await async_client.get(f"/organization/{organization_id}", headers=headers)
    assert read_response.status_code == 200
    read_data = read_response.json()
    assert read_data["name"] == "Test Organization"
    assert read_data["description"] == "An organization for testing purposes."

    # Test reading a non-existent organization
    non_existent_response = await async_client.get("/organization/invalid_id", headers=headers)
    assert non_existent_response.status_code == 404
    assert non_existent_response.json()["detail"] == "Organization not found"

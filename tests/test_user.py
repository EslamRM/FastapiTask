import pytest
from httpx import AsyncClient
from app.main import app

# Base URL for all requests
BASE_URL = "http://localhost:8080"  # Adjust to your server URL if needed


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        yield client


@pytest.mark.asyncio
async def test_signin(async_client):
    # Test valid login
    response = await async_client.post(
        "/auth/signin",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    # Test invalid login
    response = await async_client.post(
        "/auth/signin",
        json={"email": "invaliduser@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

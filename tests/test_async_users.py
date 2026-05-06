import pytest
from faker import Faker
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.users_inmemory import reset_state


@pytest.fixture(autouse=True)
def _reset_state():
    reset_state()
    yield
    reset_state()


@pytest.fixture()
def faker_instance() -> Faker:
    return Faker()


@pytest.mark.asyncio
async def test_create_user(faker_instance: Faker):
    payload = {
        "username": faker_instance.user_name(),
        "age": faker_instance.random_int(min=18, max=90),
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/users", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == payload["username"]
    assert data["age"] == payload["age"]


@pytest.mark.asyncio
async def test_get_user_ok(faker_instance: Faker):
    payload = {
        "username": faker_instance.user_name(),
        "age": faker_instance.random_int(min=18, max=90),
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        create_response = await client.post("/users", json=payload)
        user_id = create_response.json()["id"]

        response = await client.get(f"/users/{user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == payload["username"]
    assert data["age"] == payload["age"]


@pytest.mark.asyncio
async def test_get_user_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_user_ok(faker_instance: Faker):
    payload = {
        "username": faker_instance.user_name(),
        "age": faker_instance.random_int(min=18, max=90),
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        create_response = await client.post("/users", json=payload)
        user_id = create_response.json()["id"]

        response = await client.delete(f"/users/{user_id}")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_user_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.delete("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

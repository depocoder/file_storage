import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from file_storage.db.crud.user import UserCRUD
from file_storage.web.api.user.schema import UserWithPasswordScheme


@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests User instance creation."""
    url = fastapi_app.url_path_for("create_user")
    test_name = uuid.uuid4().hex
    test_password = uuid.uuid4().hex
    email = "user@example.com"
    response = await client.post(
        url,
        json={
            "username": test_name,
            "email": email,
            "password": test_password,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    serialized_response = response.json()
    user_crud = UserCRUD(dbsession)
    instances = await user_crud.get_all()
    assert instances[0].username == test_name
    assert serialized_response["password"] != test_password
    assert serialized_response["email"] == email


@pytest.mark.anyio
async def test_getting(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests user instance retrieval."""
    crud = UserCRUD(dbsession)
    test_name = uuid.uuid4().hex
    test_password = uuid.uuid4().hex
    email = "user@example.com"
    user_id_with_password = UserWithPasswordScheme(
        **{
            "username": test_name,
            "email": email,
            "password": test_password,
        }
    )

    await crud.create(user_id_with_password)
    url = fastapi_app.url_path_for("get_users")
    response = await client.get(url)
    serialized_response = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(serialized_response) == 1
    assert serialized_response[0]["username"] == test_name

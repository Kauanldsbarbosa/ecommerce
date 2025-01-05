from uuid import uuid4
from datetime import date
from fastapi import HTTPException
import pytest

from app.views.users.models import User
from app.views.users.repository import UserRepository
from app.views.users.schemas import UpdateUserSchema
from tests.views.users.fixtures import create_user
from tests.confteste import db_session


@pytest.fixture
def user_repository(db_session):
    return UserRepository(db_session)

@pytest.mark.asyncio
async def test_get_by_email(user_repository, db_session, create_user):

    fetched_user = await user_repository.get_by_email("teste@gmail.com")
    assert fetched_user is not None
    assert fetched_user.email == "teste@gmail.com"

@pytest.mark.asyncio
async def test_update_user(user_repository, db_session, create_user):

    updated_data = UpdateUserSchema(
        first_name="teste",
        last_name="teste",
        email="testenew@gmail.com",
        date_of_birth="1990-01-01"
    )

    updated_user = await user_repository.update_user(create_user.id, updated_data)

    assert updated_user.first_name == "teste"
    assert updated_user.email == "testenew@gmail.com"

@pytest.mark.asyncio
async def test_delete_user(user_repository, db_session, create_user):
    await user_repository.delete_user(create_user.id)

    deleted_user = await user_repository.get_by_email("teste@gmail.com")
    assert deleted_user is None

@pytest.mark.asyncio
async def test_validate_uuid_format():
    valid_uuid = uuid4()
    invalid_uuid = "invalid-uuid"

    assert UserRepository.validate_uuid_format(str(valid_uuid)) == valid_uuid

    with pytest.raises(HTTPException):
        UserRepository.validate_uuid_format(invalid_uuid)
        
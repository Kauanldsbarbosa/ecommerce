from datetime import date
import pytest_asyncio

from app.views.users.models import User


@pytest_asyncio.fixture
async def create_user(db_session):
    user = {
        "first_name": 'teste',
        "last_name": 'testw',
        "email": 'teste@gmail.com',
        "date_of_birth": date(2025, 1, 12),  
        "password": 'kauan1234@'
    }
    user = User(**user)
    return await user.save(db_session)
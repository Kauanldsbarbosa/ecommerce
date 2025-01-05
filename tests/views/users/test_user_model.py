import pytest
from datetime import datetime
from app.views.users.models import User

from app.utils.encrypt_pass import EncryptPass
from tests.confteste import db_session


@pytest.mark.asyncio
async def test_save_model(db_session):
    test = User(
        first_name = 'teste',
        last_name = 'testw',
        email = 'teste@gmail.com',
        date_of_birth = datetime(1990, 12, 31),
        password = 'kauan1234'
    )
    result = await test.save(db_session)
    exists_in_db =  db_session.query(User).filter(result.first_name == test.first_name).first()
    assert exists_in_db != None 
    assert result.id != None
    assert result.first_name == "teste"
    assert EncryptPass.check_password('kauan1234', result.password)
    
from http import HTTPStatus
import uuid
import pytest
from app.views.users.models import User
from app.views.users.schemas import ResponseUserSchema, UpdateUserSchema, UserBaseSchema
from tests.confteste import db_session, client
from tests.views.users.fixtures import create_user
from datetime import date, datetime



class TestEndpointUser:
    def setup_method(self):
        self.user = {
        "first_name": 'teste',
        "last_name": 'testw',
        "email": 'teste@gmail.com',
        "date_of_birth": '2025-01-02',  
        "password": 'kauan1234@'
    }
        
    def check_user_response_schema(self, reponse_data, schema:UserBaseSchema = ResponseUserSchema):

        for key, expected_type in schema.__annotations__.items():
            assert key in reponse_data, f"Key {key} not found in response."
            assert isinstance(reponse_data[key], expected_type), f"Key {key} is no type {expected_type}."

    @pytest.mark.asyncio
    async def test_view_create_user(self, db_session, client):
        response = client.post("/users", json=self.user)
        data = response.json()
        data['id'] = uuid.UUID(data['id'])

        self.check_user_response_schema(data)
        

        user_in_db = db_session.query(User).filter(User.email == self.user['email']).first()
        assert user_in_db is not None
        assert user_in_db.first_name == self.user['first_name']
        assert user_in_db.last_name == self.user['last_name']
        assert user_in_db.email == self.user['email']
        date_of_birth = datetime.strptime(self.user['date_of_birth'], '%Y-%m-%d')
        assert user_in_db.date_of_birth == date_of_birth


    @pytest.mark.asyncio
    async def test_view_create_user_with_email_already_registred(self, db_session, client):
        client.post("/users", json=self.user)
        new_user = self.user
        new_user['first_name'] = 'new'
        reponse = client.post("/users", json=self.user)
        assert reponse.status_code == 400
        assert reponse.json()['detail'] == 'Email already registered'

        created_user = db_session.query(User).filter(User.email == new_user['email']).first()
        assert created_user != None

        created_new_user = db_session.query(User).filter(User.first_name == new_user['first_name']).first()
        assert created_new_user == None

    @pytest.mark.asyncio
    async def test_view_get_user_by_id(self, db_session, client, create_user):
        assert create_user.id != None
        response = client.get(f'/users/{create_user.id}')
        assert response.status_code == 200
        data = response.json()
        data['id'] = uuid.UUID(data['id'])
        self.check_user_response_schema(data)

    @pytest.mark.asyncio
    async def test_view_get_user_by_id_invalid(self, db_session, client):
        response = client.get('/users/ceiCONSCNklcscC')
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_view_update_user_by_id(self, db_session, client, create_user):
        update_data = self.user
        update_data['email'] = 'newemail@gmail.com'
        response = client.patch(f'/users/update/{create_user.id}', json=update_data)
        assert response.status_code == 200
        self.check_user_response_schema(response, schema=UpdateUserSchema)

        updated_user = db_session.query(User).filter(User.id == create_user.id).first()

        assert updated_user.email == update_data['email']

    @pytest.mark.asyncio
    async def test_to_update_no_existent_user(self, db_session, client):
        update_data = self.user
        update_data['email'] = 'newemail@gmail.com'
        response = client.patch(f'/users/update/{uuid.uuid4()}', json=update_data)
        assert response.status_code == 400
        assert response.json()['detail'] == 'user not found'
        

    @pytest.mark.asyncio
    async def test_view_delete_user(self, db_session, client, create_user):
        response = client.delete(f'/users/delete/{create_user.id}')
        assert response.status_code == 200
        assert response.json()['message'] == 'Request was successful!'

    @pytest.mark.asyncio
    async def test_view_delete_no_existent_user(self, db_session, client):
        response = client.delete(f'/users/delete/{uuid.uuid4()}')
        assert response.status_code == 400
        assert response.json()['detail'] == 'user not found'
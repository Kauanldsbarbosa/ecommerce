# import pytest
# from sqlalchemy import Column, String
# from app.models.base_model.base_model import BaseModel

# from tests.confteste import db_session

# class TestModel(BaseModel):
#     __tablename__ = 'test'
#     name = Column(String(length=100), nullable=False, index=True)

# @pytest.fixture
# async def create_a_model_test(db_session):
#     test = TestModel(name='teste')
#     save = await test.save(db_session)
#     return save
    

# class TestBaseModel:
#     def setup_method(self):
#         self.model_test = TestModel

#     @pytest.mark.asyncio
#     async def test_save_model(self, db_session):
#         test = self.model_test(name="test")
#         result = await test.save(db_session)

#         exists_in_db =  db_session.query(self.model_test).filter(result.name == test.name).first()
#         assert result.name == "test"
#         assert result.id != None
#         assert exists_in_db != None
#         assert isinstance(result, self.model_test)

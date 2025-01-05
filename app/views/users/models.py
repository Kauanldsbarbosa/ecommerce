from sqlalchemy import Column, DateTime, String
from app.models.base_model.base_model import BaseModel
from app.utils.encrypt_pass import EncryptPass


class User(BaseModel):
    __tablename__ = 'users'
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, unique=True, nullable=False)
    date_of_birth = Column(DateTime)
    password = Column(String, nullable=False)

    def save(self, session):
        self.password = EncryptPass.hash_password(self.password)
        self.password = self.password.decode("utf-8")
        return super().save(session)
    
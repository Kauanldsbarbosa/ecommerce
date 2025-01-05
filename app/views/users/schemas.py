from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    date_of_birth: Optional[date] 

class CreateUserSchema(UserBaseSchema):
    password: str

class ResponseUserSchema(UserBaseSchema):
    id: UUID
    
class UpdateUserSchema(UserBaseSchema):
    ...

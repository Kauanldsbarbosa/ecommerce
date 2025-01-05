from http import HTTPStatus
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from app.models.base_repository import BaseRepository
from app.views.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.views.users.schemas import UpdateUserSchema



class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, User)
    async def get_by_email(self, email:str):
        statement = select(self.model_class).filter(self.model_class.email == email)
        if isinstance(self.db, AsyncSession):
            result = await self.db.execute(statement)
        
        else:
            result = self.db.execute(statement)
        return result.scalars().first()
    
    async def update_user(self, id:UUID, updated_data: UpdateUserSchema):
        user = self.db.query(self.model_class).filter_by(id=id).first()
        if user:
            try:
                user.first_name = updated_data.first_name
                user.last_name = updated_data.last_name
                user.email = updated_data.email
                user.date_of_birth = updated_data.date_of_birth
                self.db.commit()
                return user
            except:
                raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="internal error."
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="user not found"
            )
        
    async def delete_user(self, id:UUID):
        user = self.db.query(self.model_class).filter_by(id=id).first()
        if user:
            try:
                self.db.delete(user)
                self.db.commit()
            except:
                    raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail="internal error."
                )
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="user not found"
            )

    @staticmethod
    def validate_uuid_format(user_id: str) -> UUID:
        try:
            return UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Invalid UUID format."
            )

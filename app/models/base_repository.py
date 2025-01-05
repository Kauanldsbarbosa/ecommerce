from typing import Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.models.base_model.base_model import BaseModel


class BaseRepository:
    def __init__(self, db:Union[AsyncSession, Session], model_class: type[BaseModel]):
        self.db = db
        self.model_class = model_class

    async def get_by_id(self, id):
        query = select(self.model_class).where(self.model_class.id == id)
        if isinstance(self.db, AsyncSession):
            result = await self.db.execute(query)
            return result.scalars().one_or_none()
        else:
            return self.db.execute(query).scalar_one_or_none()
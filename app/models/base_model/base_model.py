from typing import Self
from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from app.models import Model
from app.utils.models_utils.model_save_manager import ModelCommitSyncManager


class BaseModel(Model):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    
    async def save(self, session) -> Self:
        try:
            session.add(self)
            await ModelCommitSyncManager.commit_session(session, self)
        except Exception as e:
            await ModelCommitSyncManager.rollback_session(session)
            raise e
        return self
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
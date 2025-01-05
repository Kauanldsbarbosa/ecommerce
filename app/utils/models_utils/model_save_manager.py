from sqlalchemy.ext.asyncio import AsyncSession


class ModelCommitSyncManager:
    @staticmethod
    async def commit_session(session, object):
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(object)
        else:
            session.commit()
            session.refresh(object)
    
    @staticmethod
    async def rollback_session(session):
        if isinstance(session, AsyncSession):
            await session.rollback()
        else:
            session.rollback()
            
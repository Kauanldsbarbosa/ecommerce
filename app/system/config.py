from app.settings import get_environment


settings = get_environment()

class Config:
    PROJECT_NAME: str = settings.PROJECT_NAME
    DATABASE_URL: str = settings.DATABASE_URL

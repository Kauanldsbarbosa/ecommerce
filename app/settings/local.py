import os
from app.settings.base import BaseConfig


class LocalSettings(BaseConfig):
    def __init__(self):
        super().__init__()
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "DEVELOPMENT-API-local")
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./src/local.db")
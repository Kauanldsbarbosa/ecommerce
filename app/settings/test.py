import os
from app.settings.base import BaseConfig


class TestSettings(BaseConfig):
    def init(self):
        super().__init__()
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///:memory:")

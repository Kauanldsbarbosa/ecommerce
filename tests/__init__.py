from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base_model.base_model import BaseModel


DATABASE_URL = "sqlite:///databaseteste.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
metadata_base_model = BaseModel.metadata
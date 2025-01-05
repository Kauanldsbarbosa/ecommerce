import os
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import Column, String
from app.main import app
from app.system.database.connection import get_db
from tests import SessionLocal, engine
from app.models import metadata

@pytest.fixture
def db_session():
    metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    metadata.drop_all(bind=engine)
    if os.path.exists("databaseteste.db"):
        os.remove("databaseteste.db")


@pytest.fixture
def client(db_session):
    def get_session_overide():
        return db_session
    
    with TestClient(app) as client:
        app.dependency_overrides[get_db] = get_session_overide
        yield client

    app.dependency_overrides.clear()

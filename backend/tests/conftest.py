import os
import sys
from pathlib import Path

os.environ.setdefault("SECRET_KEY", "isolated-test-signing-key-with-32-characters")
os.environ["DATABASE_URL"] = "sqlite://"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app
from app.models import User
from app.core.security import hash_password


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    factory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    with factory() as db:
        for username, role in (("admin", "admin"), ("user", "user")):
            db.add(User(username=username, password=hash_password("test-password"), seclevel=role))
        db.commit()

    def database():
        with factory() as db:
            yield db

    app.dependency_overrides[get_db] = database
    client = TestClient(app)
    yield client
    client.close()
    app.dependency_overrides.clear()
    engine.dispose()

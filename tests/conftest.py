import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from database import get_session
from main import app

test_engine = create_engine(
    "sqlite:///test.db",
    connect_args={"check_same_thread": False},
)


def get_test_session():
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client():
    SQLModel.metadata.drop_all(test_engine)    # empty database for every test
    SQLModel.metadata.create_all(test_engine)
    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()           # undo the swap after the test

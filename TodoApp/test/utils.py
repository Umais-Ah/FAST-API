import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..main import app
from ..models import Todos, User

client = TestClient(app)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "Umais", "id": "1", "role": "admin"}


@pytest.fixture
def test_todo():
    db = TestingSessionLocal()

    try:
        todo = Todos(
            title="Learn to code",
            description="Need to learn every day",
            priority=5,
            complete=False,
            owner_id=1,
        )

        db.add(todo)
        db.commit()

        yield todo

    finally:
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM todos"))
        db.close()


@pytest.fixture()
def test_users():
    db = TestingSessionLocal()
    try:
        user = User(
            username="Umais Ahmed",
            email="umaisahmed180@gmail.com",
            first_name="Umais",
            last_name="Ahmed",
            hashed_password=bcrypt_context.hash("umais"),
            is_active=True,
            role="admin",
            phone_number="12345678",
        )
        db.add(user)
        db.commit()

        yield user

    finally:
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM users"))
        db.close()

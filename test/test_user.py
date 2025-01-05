# test/test_user.py

import pytest
from app import app, db
from models.user import User

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def init_db():
    db.create_all()
    yield db
    db.drop_all()

def test_user_creation(init_db):
    user = User(username="test_user", password="password")
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.username == "test_user"

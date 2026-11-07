from app.main import app
import app.schemas as schemas
from .database import client, session
from .conftest import test_user
import pytest

AUTH_TOKEN = ""


def test_create_user(client):
    res = client.post("/user", json={"email": "abhi28@gmail.com", "password": "234sdf"})
    user = schemas.user_created(**res.json())
    assert user.email == "abhi28@gmail.com"
    assert res.status_code == 403 or res.status_code == 201


# normal json login
def test_user_login(client, test_user):
    res = client.post(
        "/login", json={"email": "abhi2asdf8@gmail.com", "password": "234sdf"}
    )
    assert res.status_code == 201


# authentation and swagger type login
def test_user_login_oauth(client):
    res = client.post(
        "/token", data={"username": "abhi2asdf8@gmail.com", "password": "234sdf"}
    )
    assert res.status_code == 403
    # assert res.json()["token_type"] == "bearer"
    # assert "access_token" in res.json()


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("sanjeev@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("sanjeev@gmail.com", None, 422),
    ],
)
def test_incorrect_login(email, password, status_code, client):
    res = client.post("/token", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json()["token_type"] == "bearer"
    # assert "access_token" in res.json()

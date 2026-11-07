import pytest
from app.oauth2 import create_access_token
from .database import client, session
from app import schemas


# client who is authorize ## add header
@pytest.fixture
def test_user(client):
    res = client.post(
        "/user", json={"email": "abhi2asdf8@gmail.com", "password": "234sdf"}
    )
    new_user = res.json()

    # new_user = schemas.user_created(**res.json())
    return new_user


# dont need login direct jwt from this step for authorize user
@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})


@pytest.fixture
def authorize_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


# for post get, post get all, delete, and update
@pytest.fixture
def test_post(authorize_client):
    res = authorize_client.post(
        "/posts", json={"content": "content", "title": "title", "published": False}
    )

    assert res.status_code == 201
    return res.json()

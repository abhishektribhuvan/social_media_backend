from app.main import app
import app.schemas as schemas
from .conftest import authorize_client, test_user, test_post
import pytest
from .database import client, session


# test the create post
@pytest.mark.parametrize(
    "content, title, published, status_code",
    [
        ("sdfwd", "wefcdfew", 1, 201),
        ("we aw", "ytiqe", 1, 201),
        ("ewrc", "234cc ", 1, 201),
        ("sadf ", "eadvggg", 1, 201),
    ],
)
def test_create_post(authorize_client, content, title, published, status_code):
    res = authorize_client.post(
        "/posts", json={"content": content, "title": title, "published": published}
    )
    print("lasttt")
    assert res.status_code == status_code
    # assert res.json()["id"] == test_user.id


# test test all posts
def test_get_all_post(authorize_client):
    res = authorize_client.get("/posts")
    assert res.status_code == 202


# test get post


def test_get_post(authorize_client, test_post):
    id = test_post["id"]

    res = authorize_client.get(f"/posts/{id}")
    assert res.status_code == 202


# test delete post
def test_delete_post(authorize_client, test_post):
    id = test_post["id"]
    res = authorize_client.delete(f"/posts/{id}")
    assert res.status_code == 205


# test update post
@pytest.mark.parametrize(
    "content, title, published, status_code",
    [
        ("sdfwd", "wefcdfew", False, 202),
    ],
)
def test_update_post(
    authorize_client, test_post, content, title, published, status_code
):
    id = test_post["id"]
    res = authorize_client.put(
        f"/posts/{id}",
        json={
            "content": content,
            "title": title,
            "published": published,
        },
    )
    print("lasttt")
    assert res.status_code == status_code


# test test all posts
def test_unauth_get_all_post(client):
    print("lasttt")
    res = client.get("/posts")
    assert res.status_code == 401
    print("lasttt")

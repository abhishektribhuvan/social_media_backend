from app.main import app
import app.schemas as schemas
from .database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json().get('messege'))

    assert res.json().get('messege') == "hello world"

    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/user", json={
        "email":"abhi28@gmail.com",
        "password":"234sdf"
    })

    user = schemas.user_created(**res.json())
    #print(res.json().get('messege'))

    #assert res.json().post('messege') == "hello world"
    assert user.email == "abhi28@gmail.com"
    assert res.status_code == 403 or  res.status_code == 201
#normal json login
def test_user_login(client):
    res = client.post("/login", json={
        "email": "abhi28@gmail.com",
        "password": "234sdf"
    })

    assert res.status_code == 201
    assert res.json()["token_type"] == "bearer"
    assert "access_token" in res.json()

#authentation and swagger type login
def test_user_login_oauth(client):
    res = client.post("/token", data={
        "username": "abhi28@gmail.com",
        "password": "234sdf"
    })

    assert res.status_code == 200
    assert res.json()["token_type"] == "bearer"
    assert "access_token" in res.json()    


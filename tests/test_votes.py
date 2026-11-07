from .conftest import authorize_client, test_user, test_post


def test_give_vote(authorize_client, test_post):
    id = test_post["id"]
    res = authorize_client.post("/vote", json={"vote": 1, "post_id": id})
    print("❤️❤️❤️❤️")
    assert res.status_code == 200
    res = authorize_client.post("/vote", json={"vote": 0, "post_id": id})
    print(res.json())
    assert res.status_code == 200
    # assert res.json()["id"] == test_user.id


# test test all posts
# def test_check_vote(authorize_client):
#     res = authorize_client.get("/posts")
#     assert res.status_code == 202

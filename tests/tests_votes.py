import pytest
from FastAPI90 import models

@pytest.fixture
def voted_post(create_post,session,test_user):
    new_vote =  models.Votes(post_id = create_post[0].id , user_id = test_user["id"])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client,create_post):
    res = authorized_client.post("/votes/",json= {"post_id" : f"{create_post[0].id}" , "dir" : "1"})

    assert res.status_code == 201

def test_vote_twice_vote(authorized_client,create_post,voted_post):
    res = authorized_client.post("/votes/",json= {"post_id" : f"{create_post[0].id}" , "dir" : "1"})
    assert res.status_code == 409

def test_unvote_vote(authorized_client,create_post,voted_post):
    res = authorized_client.post("/votes/",json= {"post_id" : f"{create_post[0].id}" , "dir" : "0"})
    assert res.status_code == 201

def test_delete_vote_nonexist_post(authorized_client,test_user,create_post):
    res = authorized_client.post("/votes/", json={"post_id": "1000000", "dir": "1"})
    assert res.status_code == 404

def test_delete_vote_non_exist_post(authorized_client,test_user,create_post):
    res = authorized_client.post("/votes/", json={"post_id": create_post[0].id, "dir": "0"})
    assert res.status_code == 404

def test_unauthenticated_user_can_not_vote(client,create_post):
    res = client.post("/votes/", json={"post_id": create_post[0].id, "dir": "0"})
    assert res.status_code == 401


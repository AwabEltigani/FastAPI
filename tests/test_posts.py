import pytest

from FastAPI90 import schemas


def test_get_all_posts(authorized_client,create_post):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate,res.json())
    print(list(post_map))
    assert len(res.json()) == 3
    assert res.status_code == 200

def test_unauth_user_get_post_all(client,create_post):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauth_user_get_post(client,create_post):
    res = client.get(f"/posts/{create_post[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,create_post):
    res = authorized_client.get(f"/posts/99996666699999999")
    assert res.status_code == 404

def test_for_exsiting_post(authorized_client,create_post):
    res = authorized_client.get(f"/posts/{create_post[0].id}")
    post = schemas.PostOut(**res.json())
    print(post)
    assert post.post.id == create_post[0].id

@pytest.mark.parametrize("title,content,published",[
    ("awesome new title","awesome new content", True),
    ("favoriate pizza","I love pepperoni",False),
    ("tallest skyscrapper","Burj Khalifa",True)
])
def test_create_post(authorized_client,test_user,create_post,title,content,published):
    res = authorized_client.post("/posts/",json = {"title":title,
                                                   "content":content,
                                                   "published":published})
    created_Post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_Post.title == title
    assert created_Post.content == content
    assert created_Post.owner_id == test_user["id"]

@pytest.mark.parametrize("title,content",[
    ("awesome new title","awesome new content"),
    ("favoriate pizza","I love pepperoni"),
    ("tallest skyscrapper","Burj Khalifa")
])
def test_create_post_default_published_true(authorized_client,test_user,create_post,title,content):
    res = authorized_client.post("/posts/",json={"title":title,"content":content})
    created_post = schemas.PostCreate(**res.json())
    assert res.status_code == 201
    assert created_post.published == True

@pytest.mark.parametrize("title,content",[
    ("awesome new title","awesome new content"),
    ("favoriate pizza","I love pepperoni"),
    ("tallest skyscrapper","Burj Khalifa")
])
def test_unauthorized_user_create_post(client,test_user,create_post,title,content):
    res = client.post("/posts/",json={"title":title,"content":content})

    assert res.status_code == 401

def test_unauthorized_user_delete_post(client,test_user,create_post):
    res = client.delete(f"/posts/{create_post[0].id}")
    assert res.status_code == 401

def test_authorized_user_delete_post_success(authorized_client,test_user,create_post):
    res = authorized_client.delete(f"/posts/{create_post[0].id}")

    assert res.status_code == 204

def test_delete_user_post_not_exist(authorized_client,test_user,create_post):
    res = authorized_client.delete("/posts/10000000000000")

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_user,create_post,test_user_2):
    res = authorized_client.delete(f"/posts/{create_post[2].id}")

    assert res.status_code == 403

def test_update_post(authorized_client,test_user,create_post):
    res = authorized_client.put(f"/posts/{create_post[0].id}",json={"title":"updated post","content":"changed my mind","published":"True"})

    print(res.json())

    assert res.status_code == 200

def test_update_other_user_post(authorized_client,test_user,test_user_2,create_post):
    res = authorized_client.put(f"/posts/{create_post[2].id}",
                                json={"title": "updated post", "content": "changed my mind", "published": "True"})


    assert res.status_code == 403

def test_update_unauthorized_user_post(client,test_user,test_user_2,create_post):
    res = client.put(f"/posts/{create_post[0].id}",
                                json={"title": "updated post", "content": "changed my mind", "published": "True"})


    assert res.status_code == 401

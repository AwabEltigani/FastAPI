
import pytest
from starlette.testclient import TestClient

from FastAPI90 import models
from FastAPI90.database import Base, get_db
from FastAPI90.main import app
from tests.database import TestingSessionLocal, test_engine
from FastAPI90.oauth2 import create_access_token


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()  # What is responsible for connecting with our database
    # when it gets called it connects to our database allows us to communicate with it
    # when we are done it closes the connection to our database avoiding any errors
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client(session):
    #run our code before we return our test client
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # run our code after our test finishes
    #drops all our tables

@pytest.fixture
def test_user(client):
    user_data = {"email": "username123@gmail.com",
                 "password" : "password123",
                 "phone_num" : "757-839-6417"}
    res = client.post("/users/",json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user_2(client):
    user_data = {
        "email":"username123123@gmail.com",
        "password":"123123123",
        "phone_num":"757-987-1234"
    }
    res = client.post("/users/",json=user_data)
    new_user2 = res.json()
    return new_user2

@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture()
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture()
def create_post(test_user, session, test_user_2):
    post_data = [
        {"title": "Post 1", "content": "Content for post 1", "owner_id": test_user['id']},
        {"title": "Post 2", "content": "Content for post 2", "owner_id": test_user['id']},

        {"title": "Post 3", "content": "Content for post 3", "owner_id": test_user_2['id']}
    ]
    def create_post_model(post):
        return models.Post(**post)


    post_map = map(create_post_model,post_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()





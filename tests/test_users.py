import os





from jose import jwt
from FastAPI90.oauth2 import Algorithm, Secret_Key
from FastAPI90 import schemas
from tests.conftest import client,session,test_user
import pytest


#
# def test_root(client,session):
#     res = client.get("/")
#     assert (res.json().get('message')) == "Welcome to my api"
#     assert res.status_code == 200





def test_create_users(client,session):
    res = client.post("/users/",json = { "email":"usernme3543@gmail.com",
                                            "password":"password123",
                                            "phone_num":"656-86097"})
    new_user = schemas.UserResponse(**res.json())

    assert new_user.email == "usernme3543@gmail.com"
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post("/login/",data = { "username":test_user['email'],
                                            "password":test_user['password']
                                            })
    login_response = schemas.Token(**res.json())
    payload = jwt.decode(login_response.access_token, Secret_Key, algorithms=[Algorithm])
    id = payload.get("user_id")  ##in the payload we passed it in as userdata when
    assert  id == test_user['id']
    assert login_response.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    (None, "password123", 401),                     # Missing email
    ("invalidemail", "password123", 401),         # Invalid email format
    ("testuser@gmail.com", "", 401),              # Missing password
    ("", "", 401),                                # Missing both fields
    ("testuser@gmail", "123", 401),               # Invalid email & too short password
    ("@gmail.com", "pw", 401),                    # Bad email format & weak password
])
def test_incorrect_login(client,email,password,status_code):
    res = client.post("/login",data = {"username" : email,
                                            "password" : password})
    assert res.status_code == status_code





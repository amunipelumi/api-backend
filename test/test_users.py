import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello! Welcome to the homepage...'
    assert res.status_code == 200

def test_create_user(client):
    user_data = {
        "username": "hello123", 
        "email": "hello123@email.com", 
        "password": "hello123password"
    }
    res = client.post(
        "/users/register/", json=user_data
    )
    print(res.json())
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "hello123@email.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    data={"username": test_user['username'], "password": test_user['password']}
    res = client.post(
        "/login", data=data
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, 
                         algorithms=[settings.algorithm])
    username = payload.get("username")

    assert username == test_user['username']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("username, password, status_code", [
    ('wrong', 'password123', 403),
    ('sami', 'wrongpassword', 403),
    ('wrong', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('santos', None, 422)
])
def test_incorrect_login(client, username, password, status_code):
    res = client.post(
        "/login", data={"username": username, "password": password}
    )
    # print(res.json().get('detail'))
    assert res.status_code == status_code

from fastapi import status

from TodoApp.routers.users import get_current_user, get_db

from .utils import *

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


def test_return_user(test_users):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "Umais Ahmed"
    assert response.json()["email"] == "umaisahmed180@gmail.com"
    assert response.json()["first_name"] == "Umais"
    assert response.json()["last_name"] == "Ahmed"
    assert response.json()["is_active"] == True
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "12345678"


def test_change_password_success(test_users):
    response = client.put(
        "/users/", json={"password": "umais", "new_password": "umais123"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_users):
    response = client.put(
        "/users/", json={"password": "wrong_password", "new_password": "umais123"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_sucess(test_users):
    response = client.put("/users/phonenumber/22222222")
    response.status_code = status.HTTP_204_NO_CONTENT

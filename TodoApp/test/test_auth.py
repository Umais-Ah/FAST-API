from datetime import timedelta

from fastapi import HTTPException
from jose import jwt

from ..routers.auth import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from .utils import *


def test_authenticate_user(test_users):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_users.username, "umais", db)
    assert authenticated_user is not None

    non_existent_user = authenticate_user("WrongUserName", "umais", db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_users.username, "wrongpassword", db)
    assert wrong_password_user is False


def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)
    decode_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decode_token.get("id") == user_id
    assert decode_token.get("sub") == username
    assert decode_token.get("role") == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "test_user", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {"username": "test_user", "id": 1, "role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate user"

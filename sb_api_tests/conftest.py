import os
import random
import string
from typing import Dict, List, Tuple

import pytest
import requests

from utils.endpoints import (
    AUTH_REGISTER,
    AUTH_LOGIN,
    AUTH_USER,
    INGREDIENTS,
)


def _rand(n: int = 10) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


def _delete_user(access_token: str) -> None:
    if not access_token:
        return
    headers = {"Authorization": access_token}
    try:
        requests.delete(AUTH_USER, headers=headers, timeout=10)
    except Exception:
        pass


@pytest.fixture
def unique_user_payload() -> Dict[str, str]:
    email = f"{_rand()}@example.com"
    return {"email": email, "password": _rand(12), "name": _rand(8)}


@pytest.fixture
def user_context(unique_user_payload) -> Tuple[Dict[str, str], Dict[str, str]]:
    reg = requests.post(AUTH_REGISTER, json=unique_user_payload)
    assert reg.status_code in (200, 403)
    if reg.status_code == 403:
        unique_user_payload["email"] = f"{_rand()}@example.com"
        reg = requests.post(AUTH_REGISTER, json=unique_user_payload)
        assert reg.status_code == 200
    login_resp = requests.post(
        AUTH_LOGIN,
        json={"email": unique_user_payload["email"], "password": unique_user_payload["password"]},
    )
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    try:
        yield unique_user_payload, tokens
    finally:
        _delete_user(tokens.get("accessToken", ""))


@pytest.fixture
def auth_headers(user_context) -> Dict[str, str]:
    _, tokens = user_context
    return {"Authorization": tokens.get("accessToken", "")}


@pytest.fixture
def ingredients_list() -> List[str]:
    resp = requests.get(INGREDIENTS)
    assert resp.status_code == 200
    data = resp.json()
    return [item["_id"] for item in data.get("data", [])]

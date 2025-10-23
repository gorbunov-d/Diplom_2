from typing import Dict, List, Tuple

import pytest
import requests

from utils.endpoints import AUTH_REGISTER, AUTH_LOGIN, INGREDIENTS
from utils.helpers import delete_user, make_user_payload


@pytest.fixture
def user_context() -> Tuple[Dict[str, str], Dict[str, str]]:
    # Предусловия без assert: регистрируем и логинимся, ошибки валидирует сам тест
    payload = make_user_payload()
    reg = requests.post(AUTH_REGISTER, json=payload)
    if reg.status_code == 403:
        payload["email"] = make_user_payload()["email"]
        reg = requests.post(AUTH_REGISTER, json=payload)
    login_resp = requests.post(
        AUTH_LOGIN,
        json={"email": payload["email"], "password": payload["password"]},
    )
    tokens = login_resp.json()
    yield payload, tokens
    delete_user(tokens.get("accessToken"))


@pytest.fixture
def registered_user() -> Dict[str, str]:
    payload = make_user_payload()
    requests.post(AUTH_REGISTER, json=payload)
    yield payload
    # cleanup via login -> delete
    login_resp = requests.post(AUTH_LOGIN, json={"email": payload["email"], "password": payload["password"]})
    token = login_resp.json().get("accessToken", "") if login_resp.ok else ""
    delete_user(token)


@pytest.fixture
def auth_headers(user_context) -> Dict[str, str]:
    _, tokens = user_context
    return {"Authorization": tokens.get("accessToken", "")}


@pytest.fixture
def ingredients_list() -> List[str]:
    resp = requests.get(INGREDIENTS)
    data = resp.json() if resp.ok else {"data": []}
    return [item["_id"] for item in data.get("data", [])]


@pytest.fixture
def user_cleanup():
    created: List[Dict[str, str]] = []
    yield created
    for payload in created:
        login_resp = requests.post(AUTH_LOGIN, json={"email": payload["email"], "password": payload["password"]})
        token = login_resp.json().get("accessToken", "") if login_resp.ok else ""
        delete_user(token)

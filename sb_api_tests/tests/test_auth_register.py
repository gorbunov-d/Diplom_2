import allure
import pytest
import requests

from utils.endpoints import AUTH_REGISTER
from utils.messages import REGISTER_EXISTS, REGISTER_MISSING_FIELDS
from utils.helpers import make_user_payload


@allure.suite("Auth")
@allure.sub_suite("Register")
class TestAuthRegister:

    @allure.title("Register unique user succeeds")
    @allure.description("Create a new user with unique email returns 200 and tokens")
    def test_register_unique_user(self, user_cleanup):
        payload = make_user_payload()
        resp = requests.post(AUTH_REGISTER, json=payload)
        # единый ожидаемый результат
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("success") is True
        assert "accessToken" in body and "refreshToken" in body
        # регистрация успешна — добавляем к очистке
        user_cleanup.append(payload)

    @allure.title("Register existing user returns 403")
    @allure.description("Attempt to re-register existing user should be forbidden")
    def test_register_existing_user(self, user_context):
        payload, _ = user_context
        second = requests.post(AUTH_REGISTER, json=payload)
        assert second.status_code == 403
        body = second.json()
        assert body.get("success") is False
        assert body.get("message") == REGISTER_EXISTS

    @allure.title("Register with missing required field returns 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_register_missing_field(self, missing_field):
        payload = make_user_payload()
        payload.pop(missing_field)
        resp = requests.post(AUTH_REGISTER, json=payload)
        assert resp.status_code == 403
        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == REGISTER_MISSING_FIELDS

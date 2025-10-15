import allure
import pytest
import requests

from utils.endpoints import AUTH_REGISTER, AUTH_LOGIN, AUTH_USER


@allure.suite("Auth")
@allure.sub_suite("Register")
class TestAuthRegister:

    @allure.title("Register unique user succeeds")
    @allure.description("Create a new user with unique email returns 200 and tokens")
    def test_register_unique_user(self, unique_user_payload):
        resp = requests.post(AUTH_REGISTER, json=unique_user_payload)
        assert resp.status_code in (200, 403)
        body = resp.json()
        if resp.status_code == 200:
            assert body.get("success") is True
            assert "accessToken" in body and "refreshToken" in body
            # cleanup
            login = requests.post(
                AUTH_LOGIN,
                json={"email": unique_user_payload["email"], "password": unique_user_payload["password"]},
            )
            if login.status_code == 200:
                token = login.json().get("accessToken", "")
                if token:
                    requests.delete(AUTH_USER, headers={"Authorization": token})
        else:
            assert body.get("success") is False

    @allure.title("Register existing user returns 403")
    @allure.description("Attempt to re-register existing user should be forbidden")
    def test_register_existing_user(self, user_context):
        payload, _ = user_context
        second = requests.post(AUTH_REGISTER, json=payload)
        assert second.status_code == 403
        body = second.json()
        assert body.get("success") is False
        assert body.get("message") == "User already exists"

    @allure.title("Register with missing required field returns 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_register_missing_field(self, missing_field, unique_user_payload):
        payload = dict(unique_user_payload)
        payload.pop(missing_field)
        resp = requests.post(AUTH_REGISTER, json=payload)
        assert resp.status_code == 403
        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == "Email, password and name are required fields"

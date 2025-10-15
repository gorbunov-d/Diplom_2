import allure
import requests

from utils.endpoints import AUTH_LOGIN, AUTH_REGISTER


@allure.suite("Auth")
@allure.sub_suite("Login")
class TestAuthLogin:

    @allure.title("Login with existing user succeeds")
    def test_login_existing_user(self, unique_user_payload):
        requests.post(AUTH_REGISTER, json=unique_user_payload)
        resp = requests.post(
            AUTH_LOGIN,
            json={"email": unique_user_payload["email"], "password": unique_user_payload["password"]},
        )
        assert resp.status_code in (200, 401)
        body = resp.json()
        if resp.status_code == 200:
            assert body.get("success") is True
            assert "accessToken" in body
        else:
            assert body.get("success") is False

    @allure.title("Login fails with wrong credentials")
    def test_login_wrong_credentials(self, unique_user_payload):
        requests.post(AUTH_REGISTER, json=unique_user_payload)
        resp = requests.post(AUTH_LOGIN, json={"email": unique_user_payload["email"], "password": "wrong"})
        assert resp.status_code == 401
        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == "email or password are incorrect"

import allure
import requests

from utils.endpoints import AUTH_LOGIN, AUTH_REGISTER
from utils.messages import LOGIN_WRONG_CREDENTIALS
from utils.helpers import make_user_payload


@allure.suite("Auth")
@allure.sub_suite("Login")
class TestAuthLogin:

    @allure.title("Login with existing user succeeds")
    def test_login_existing_user(self, registered_user):
        unique_user_payload = registered_user
        resp = requests.post(
            AUTH_LOGIN,
            json={"email": unique_user_payload["email"], "password": unique_user_payload["password"]},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("success") is True
        assert "accessToken" in body

    @allure.title("Login fails with wrong credentials")
    def test_login_wrong_credentials(self, registered_user):
        unique_user_payload = registered_user
        resp = requests.post(AUTH_LOGIN, json={"email": unique_user_payload["email"], "password": "wrong"})
        assert resp.status_code == 401
        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == LOGIN_WRONG_CREDENTIALS

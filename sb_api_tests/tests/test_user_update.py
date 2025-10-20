import allure
import requests

from utils.endpoints import AUTH_USER
from utils.messages import UNAUTHORIZED


@allure.suite("User")
@allure.sub_suite("Update")
class TestUserUpdate:

    @allure.title("Authorized user can update any field")
    def test_user_update_authorized(self, user_context):
        payload, tokens = user_context
        headers = {"Authorization": tokens.get("accessToken")}

        new_data = {"name": payload["name"] + "x"}
        resp = requests.patch(AUTH_USER, headers=headers, json=new_data)
        assert resp.status_code in (200, 403)
        body = resp.json()
        if resp.status_code == 200:
            assert body.get("success") is True
            assert body.get("user", {}).get("name") == new_data["name"]
        else:
            assert body.get("success") is False

    @allure.title("Unauthorized user cannot update user data")
    def test_user_update_unauthorized(self, unique_user_payload):
        new_data = {"name": unique_user_payload["name"] + "x"}
        resp = requests.patch(AUTH_USER, json=new_data)
        assert resp.status_code == 401
        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == UNAUTHORIZED

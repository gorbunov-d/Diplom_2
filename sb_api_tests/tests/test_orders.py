import allure
import pytest
import requests

from utils.endpoints import ORDERS, AUTH_REGISTER, AUTH_LOGIN


@allure.suite("Orders")
class TestOrders:

    @allure.title("Create order with auth and valid ingredients succeeds")
    def test_create_order_with_auth(self, ingredients_list, unique_user_payload):
        requests.post(AUTH_REGISTER, json=unique_user_payload)
        login = requests.post(
            AUTH_LOGIN,
            json={"email": unique_user_payload["email"], "password": unique_user_payload["password"]},
        )
        assert login.status_code == 200
        headers = {"Authorization": login.json().get("accessToken")}

        payload = {"ingredients": ingredients_list[:2]}
        resp = requests.post(ORDERS, headers=headers, json=payload)
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("success") is True
        assert body.get("order", {}).get("number")

    @allure.title("Create order without auth")
    def test_create_order_without_auth(self, ingredients_list):
        payload = {"ingredients": ingredients_list[:2]}
        resp = requests.post(ORDERS, json=payload)
        assert resp.status_code in (200, 401)
        body = resp.json()
        if resp.status_code == 200:
            assert body.get("success") is True
        else:
            assert body.get("success") is False

    @allure.title("Create order without ingredients returns 400")
    def test_create_order_without_ingredients(self):
        resp = requests.post(ORDERS, json={"ingredients": []})
        assert resp.status_code == 400
        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == "Ingredient ids must be provided"

    @allure.title("Create order with invalid ingredient id returns error")
    def test_create_order_with_invalid_ingredient(self):
        resp = requests.post(ORDERS, json={"ingredients": ["invalid-hash"]})
        assert resp.status_code in (400, 500)
        if resp.status_code == 400:
            body = resp.json()
            assert body.get("success") is False
            assert body.get("message")

    @allure.title("Get user orders: authorized success; unauthorized 401")
    def test_get_user_orders_auth_and_unauth(self, ingredients_list, unique_user_payload):
        requests.post(AUTH_REGISTER, json=unique_user_payload)
        login = requests.post(
            AUTH_LOGIN,
            json={"email": unique_user_payload["email"], "password": unique_user_payload["password"]},
        )
        assert login.status_code == 200
        token = login.json().get("accessToken")
        headers = {"Authorization": token}

        resp_auth = requests.get(ORDERS, headers=headers)
        assert resp_auth.status_code == 200
        assert resp_auth.json().get("success") is True

        resp_unauth = requests.get(ORDERS)
        assert resp_unauth.status_code == 401
        assert resp_unauth.json().get("message") == "You should be authorised"

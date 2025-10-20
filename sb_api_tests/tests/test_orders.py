import allure
import pytest
import requests

from utils.endpoints import ORDERS
from utils.messages import ORDER_MISSING_INGREDIENTS, UNAUTHORIZED


@allure.suite("Orders")
class TestOrders:

    @allure.title("Create order with auth and valid ingredients succeeds")
    def test_create_order_with_auth(self, ingredients_list, auth_headers):
        payload = {"ingredients": ingredients_list[:2]}
        resp = requests.post(ORDERS, headers=auth_headers, json=payload)
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
    def test_create_order_without_ingredients(self, auth_headers):
        resp = requests.post(ORDERS, headers=auth_headers, json={"ingredients": []})
        assert resp.status_code == 400
        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == ORDER_MISSING_INGREDIENTS

    @allure.title("Create order with invalid ingredient id returns error")
    def test_create_order_with_invalid_ingredient(self, auth_headers):
        resp = requests.post(ORDERS, headers=auth_headers, json={"ingredients": ["invalid-hash"]})
        assert resp.status_code in (400, 500)
        if resp.status_code == 400:
            body = resp.json()
            assert body.get("success") is False
            assert body.get("message")

    @allure.title("Get user orders: authorized success; unauthorized 401")
    def test_get_user_orders_auth_and_unauth(self, auth_headers):
        resp_auth = requests.get(ORDERS, headers=auth_headers)
        assert resp_auth.status_code == 200
        assert resp_auth.json().get("success") is True

        resp_unauth = requests.get(ORDERS)
        assert resp_unauth.status_code == 401
        assert resp_unauth.json().get("message") == UNAUTHORIZED

import os

BASE = os.getenv("SB_BASE_URL", "https://stellarburgers.education-services.ru")

AUTH_REGISTER = f"{BASE}/api/auth/register"
AUTH_LOGIN = f"{BASE}/api/auth/login"
AUTH_LOGOUT = f"{BASE}/api/auth/logout"
AUTH_TOKEN = f"{BASE}/api/auth/token"
AUTH_USER = f"{BASE}/api/auth/user"

INGREDIENTS = f"{BASE}/api/ingredients"
ORDERS = f"{BASE}/api/orders"
ORDERS_ALL = f"{BASE}/api/orders/all"

PASSWORD_RESET = f"{BASE}/api/password-reset"
PASSWORD_RESET_CONFIRM = f"{BASE}/api/password-reset/reset"

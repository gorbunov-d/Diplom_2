import random
import string
from typing import Optional, Dict

import requests

from utils.endpoints import AUTH_USER


def rand(n: int = 10) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


def delete_user(access_token: Optional[str]) -> None:
    if not access_token:
        return
    headers = {"Authorization": access_token}
    try:
        requests.delete(AUTH_USER, headers=headers, timeout=10)
    except Exception:
        # Network or API hiccups should not fail teardown
        pass


def make_user_payload() -> Dict[str, str]:
    email = f"{rand()}@example.com"
    return {"email": email, "password": rand(12), "name": rand(8)}




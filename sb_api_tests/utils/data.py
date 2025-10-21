from typing import Dict

from utils.helpers import rand


def make_user_payload() -> Dict[str, str]:
    email = f"{rand()}@example.com"
    return {"email": email, "password": rand(12), "name": rand(8)}



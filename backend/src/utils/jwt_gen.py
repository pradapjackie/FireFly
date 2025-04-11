from datetime import datetime, timedelta, UTC
from pathlib import Path

from jose import jwt


def generate_jwt_token(key_path: Path, user_id: str):
    issued_at = int((datetime.now(UTC) - timedelta(days=30)).timestamp())
    with open(key_path, "r") as private_key:
        return jwt.encode({"iat": issued_at, "sub": str(user_id)}, private_key.read(), algorithm="RS256")

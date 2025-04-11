import hashlib
import hmac


def sha1(string: str) -> str:
    return hashlib.sha1(string.encode("utf-8")).hexdigest()


def sha256(string: str) -> str:
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


def md5(string: str) -> str:
    return hashlib.md5(string.encode("utf-8")).hexdigest()


def hmac_sha256(string: str, salt: str) -> str:
    return hmac.new(salt.encode("UTF-8"), string.encode("UTF-8"), hashlib.sha256).hexdigest()

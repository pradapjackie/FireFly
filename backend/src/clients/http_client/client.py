from http.cookies import SimpleCookie
from typing import Optional, Self

from aiohttp import ClientSession, CookieJar


class HttpClient:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._http_session: Optional[ClientSession] = None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    @property
    def http_session(self):
        if not self._http_session or self._http_session.closed:
            self._http_session = ClientSession(*self.args, **self.kwargs)
        return self._http_session

    async def close(self):
        self._http_session and await self._http_session.close()

    def add_cookie(self, name, value, **kwargs):
        cookie = SimpleCookie()
        cookie[name] = value
        for param_name, param_value in kwargs.items():
            cookie[name][param_name] = param_value
        self.http_session.cookie_jar.update_cookies(cookie)

    def get_cookie(self, name: str) -> str | None:
        for cookie in self.http_session.cookie_jar:
            if cookie.key == name:
                return cookie.value

    def copy_cookies(self, cookie_jar: CookieJar):
        for cookie in cookie_jar:
            self.add_cookie(name=cookie.key, value=cookie.value, path=cookie["path"], domain=cookie["domain"])

    def clear_cookie(self):
        self.http_session.cookie_jar.clear()

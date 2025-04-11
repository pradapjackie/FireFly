import json
from json import JSONDecodeError
from typing import Any, Tuple

from arsenic.connection import check_response_error, ensure_task, log, strip_auth, wrap_screen


@ensure_task
async def request(self, *, url: str, method: str, data=None, timeout=None) -> Tuple[int, Any]:
    header = {"Content-Type": "application/json; charset=utf-8"}
    if data is None:
        data = {}
    if method not in {"POST", "PUT"}:
        data = None
        header = None
    body = json.dumps(data) if data is not None else None
    full_url = self.prefix + url
    log.info("request", url=strip_auth(full_url), method=method, header=header, body=body)
    async with self.session.request(
        url=full_url, method=method, headers=header, data=body, timeout=timeout
    ) as response:
        response_body = await response.read()
        try:
            data = json.loads(response_body)
        except JSONDecodeError as exc:
            log.error("json-decode", body=response_body)
            data = {"error": "!internal", "message": str(exc), "stacktrace": ""}
        wrap_screen(data)
        log.info(
            "response",
            url=strip_auth(full_url),
            method=method,
            body=body,
            response=response,
            data=data,
        )
        check_response_error(data=data, status=response.status)
        return response.status, data

import datetime
from http.client import (
    BAD_REQUEST,
    INTERNAL_SERVER_ERROR,
    REQUEST_TIMEOUT,
    UNAUTHORIZED,
)
from typing import Any

import orjson
from httpx import AsyncClient, HTTPStatusError, Response
from pydantic import Field

from iikocloudapi.helpers import BaseResponseModel

TOKEN_EXPIRES_TIME = datetime.timedelta(minutes=15)
DEFAULT_API_URL = "https://api-ru.iiko.services"
BASE_HEADERS = {
    "Content-Type": "application/json",
    "Timeout": "15",
}


class ErrorDataModel(BaseResponseModel):
    error_description: str = Field(alias="errorDescription")
    error: str | None = None


class HTTPError(Exception):
    def __init__(self, error_data: ErrorDataModel, http: HTTPStatusError) -> None:
        self.error_data = error_data
        self.http = http


class AccessTokenResponse(BaseResponseModel):
    token: str


class TokenInfo:
    def __init__(self, access_data: AccessTokenResponse) -> None:
        self.access_data = access_data
        self.time = datetime.datetime.now(datetime.UTC)

    def is_expired(self) -> bool:
        delta = datetime.datetime.now(datetime.UTC) - TOKEN_EXPIRES_TIME
        return delta > self.time


class Client:
    def __init__(
        self,
        api_login: str,
        api_url: str = DEFAULT_API_URL,
        headers: dict[str, str] | None = None,
        session: AsyncClient | None = None,
    ) -> None:
        self.api_login = api_login
        self.api_url = api_url.strip("/ ")
        self.headers = headers or BASE_HEADERS
        if not session:
            self.session = AsyncClient(headers=self.headers)
        else:
            self.session = session
        self.token_info: TokenInfo | None = None

    async def access_token(self, api_login: str | None = None) -> AccessTokenResponse:
        response = await self.request(
            "/api/1/access_token",
            data={"apiLogin": api_login or self.api_login},
            auth=False,
        )
        return AccessTokenResponse(**orjson.loads(response.content))

    async def auth(self):
        access_data = await self.access_token()
        self.token_info = TokenInfo(access_data)
        self.headers["Authorization"] = f"Bearer {access_data.token}"

    async def request(
        self,
        path: str,
        method: str = "POST",
        data: Any = None,
        timeout: str | int | None = None,
        *,
        auth: bool = True,
    ) -> Response:
        if auth and (not self.token_info or self.token_info.is_expired()):
            await self.auth()

        headers = self.headers
        if timeout:
            headers = self.headers.copy()
            headers["Timeout"] = str(timeout)

        content = None
        if data:
            content = orjson.dumps(data)

        response = await self.session.request(method, self.build_path(path), content=content, headers=headers)

        try:
            response.raise_for_status()
        except HTTPStatusError as err:
            if err.response.status_code == UNAUTHORIZED and auth:
                await self.auth()
                return await self.request(path, data=data, timeout=timeout, auth=False)
            if err.response.status_code in (
                UNAUTHORIZED,
                BAD_REQUEST,
                REQUEST_TIMEOUT,
                INTERNAL_SERVER_ERROR,
            ):
                raise HTTPError(
                    error_data=ErrorDataModel(**orjson.loads(err.response.content)),
                    http=err,
                ) from err
            raise
        return response

    def build_path(self, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.api_url}{path}"

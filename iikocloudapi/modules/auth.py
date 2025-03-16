from iikocloudapi.client import AccessTokenResponse, Client


class Auth:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def access_token(self, api_login: str) -> AccessTokenResponse:
        return await self._client.access_token(api_login)

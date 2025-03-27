from iikocloudapi.client import AccessTokenResponse, Client


class Auth:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def access_token(self, api_login: str) -> AccessTokenResponse:
        """Retrieve session key for API user.

        Args:
            api_login (str): API key. It is set in iikoWeb.

        Ref: https://api-ru.iiko.services/#tag/Authorization/paths/~1api~11~1access_token/post
        """
        return await self._client.access_token(api_login)

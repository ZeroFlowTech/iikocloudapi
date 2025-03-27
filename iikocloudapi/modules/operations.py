from typing import Literal

import orjson
from pydantic import BaseModel

from iikocloudapi.client import Client


class CommandsStatusResponse(BaseModel):
    state: Literal["InProgress", "Success", "Error"]
    exception: str | None = None


class Operations:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def commands_status(
        self,
        organization_id: str,
        correlation_id: str,
        timeout: str | int | None = None,
    ) -> CommandsStatusResponse:
        response = await self._client.request(
            "/api/1/commands/status",
            data={
                "organizationId": organization_id,
                "correlationId": correlation_id,
            },
            timeout=timeout,
        )
        return CommandsStatusResponse(**orjson.loads(response.content))

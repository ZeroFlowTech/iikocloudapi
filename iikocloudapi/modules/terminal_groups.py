import orjson
from pydantic import BaseModel, Field

from iikocloudapi.client import Client
from iikocloudapi.helpers import BaseResponseModel, ExternalData


class Terminal(BaseModel):
    id: str
    organization_id: str = Field(alias="organizationId")
    name: str
    timezone: str = Field(alias="timeZone")
    external_data: list[ExternalData] | None = Field(None, alias="externalData")


class TerminalGroupsResponse(BaseResponseModel):
    class TerminalGroup(BaseModel):
        organization_id: str = Field(alias="organizationId")
        items: list[Terminal]

    terminal_groups: list[TerminalGroup] = Field(alias="terminalGroups")
    terminal_groups_in_sleep: list[TerminalGroup] = Field(alias="terminalGroupsInSleep")


class IsAliveStatus(BaseModel):
    is_alive: bool = Field(alias="isAlive")
    terminal_group_id: str = Field(alias="terminalGroupId")
    organization_id: str = Field(alias="organizationId")


class TerminalIsAliveResponse(BaseResponseModel):
    is_alive_status: list[IsAliveStatus] = Field(alias="isAliveStatus")


class TerminalAwakeResponse(BaseModel):
    successfully_processed: list[str] | None = Field(
        None, alias="successfullyProcessed"
    )
    failed_processed: list[str] | None = Field(None, alias="failedProcessed")


class TerminalGroups:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def __call__(
        self,
        organization_ids: list[str],
        include_disabled: bool | None = None,
        return_external_data: list[str] | None = None,
        timeout: str | int | None = None,
    ) -> TerminalGroupsResponse:
        response = await self._client.request(
            "/api/1/terminal_groups",
            data={
                "organizationIds": organization_ids,
                "includeDisabled": include_disabled,
                "returnExternalData": return_external_data,
            },
            timeout=timeout,
        )
        return TerminalGroupsResponse(**orjson.loads(response.content))

    async def is_alive(
        self,
        terminal_group_ids: list[str],
        organization_ids: list[str],
        timeout: str | int | None = None,
    ) -> TerminalIsAliveResponse:
        response = await self._client.request(
            "/api/1/terminal_groups/is_alive",
            data={
                "organizationIds": organization_ids,
                "terminalGroupIds": terminal_group_ids,
            },
            timeout=timeout,
        )
        return TerminalIsAliveResponse(**orjson.loads(response.content))

    async def awake(
        self,
        terminal_group_ids: list[str],
        organization_ids: list[str],
        timeout: str | int | None = None,
    ) -> TerminalAwakeResponse:
        response = await self._client.request(
            "/api/1/terminal_groups/awake",
            data={
                "organizationIds": organization_ids,
                "terminalGroupIds": terminal_group_ids,
            },
            timeout=timeout,
        )
        return TerminalAwakeResponse(**orjson.loads(response.content))

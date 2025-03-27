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
        """Method that returns information on groups of delivery terminals.

        Args:
            organization_ids (list[str]): Organizations IDs for which information is requested.
                Can be obtained by `/api/1/organizations` operation.
            include_disabled (bool | None, optional): Attribute that shows that response
                contains disabled terminal groups.
                Defaults to None.
            return_external_data (list[str] | None, optional): External data keys that have to be returned.
                Defaults to None.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Terminal-groups/paths/~1api~11~1terminal_groups/post
        """
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
        organization_ids: list[str],
        terminal_group_ids: list[str],
        timeout: str | int | None = None,
    ) -> TerminalIsAliveResponse:
        """Returns information on availability of group of terminals.

        Args:
            organization_ids (list[str]): Organization IDs.
                Can be obtained by `/api/1/organizations` operation.
            terminal_group_ids (list[str]): List of terminal groups IDs.
                Can be obtained by `/api/1/terminal_groups` operation.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Terminal-groups/paths/~1api~11~1terminal_groups~1is_alive/post
        """
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
        organization_ids: list[str],
        terminal_group_ids: list[str],
        timeout: str | int | None = None,
    ) -> TerminalAwakeResponse:
        """_summary_

        Args:
            organization_ids (list[str]):  Organization IDs.
                Can be obtained by `/api/1/organizations` operation.
            terminal_group_ids (list[str]): List of terminal groups IDs.
                Can be obtained by `/api/1/terminal_groups` operation.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Terminal-groups/paths/~1api~11~1terminal_groups~1awake/post
        """
        response = await self._client.request(
            "/api/1/terminal_groups/awake",
            data={
                "organizationIds": organization_ids,
                "terminalGroupIds": terminal_group_ids,
            },
            timeout=timeout,
        )
        return TerminalAwakeResponse(**orjson.loads(response.content))

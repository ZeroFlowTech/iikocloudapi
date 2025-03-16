import orjson
from pydantic import BaseModel, Field

from iikocloudapi.client import Client


class SendResponse(BaseModel):
    correlation_id: str = Field(alias="correlationId")


class Notifications:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def send(
        self,
        order_source: str,
        order_id: str,
        additional_info: str,
        message_type: str,
        organization_id: str,
        timeout: str | int | None = None,
    ) -> SendResponse:
        response = await self._client.request(
            "/api/1/notifications/send",
            data={
                "orderSource": order_source,
                "orderId": order_id,
                "additionalInfo": additional_info,
                "messageType": message_type,
                "organizationId": organization_id,
            },
            timeout=timeout,
        )
        return SendResponse(**orjson.loads(response.content))

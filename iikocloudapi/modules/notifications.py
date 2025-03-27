import orjson

from iikocloudapi.client import Client
from iikocloudapi.helpers import BaseResponseModel


class SendResponse(BaseResponseModel):
    pass


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
        """Send notification to external systems (iikoFront and iikoWeb).

        Args:
            order_source (str): Order source.
            order_id (str): Order ID.
            additional_info (str): Additional info about the problem.
            message_type (str): Message type.
            organization_id (str): Organization UOC Id.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Notifications/paths/~1api~11~1notifications~1send/post
        """
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

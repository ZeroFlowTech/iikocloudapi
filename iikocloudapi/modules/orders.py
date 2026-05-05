from collections.abc import Mapping
from typing import Any, Literal

import orjson
from pydantic import BaseModel, ConfigDict, Field

from iikocloudapi.client import Client
from iikocloudapi.helpers import BaseResponseModel


class OrderCreateModifier(BaseModel):
    """Modifier line inside an order item (`order.items[].modifiers`)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    product_id: str = Field(alias="productId")
    amount: float = 1.0


class OrderCreateItem(BaseModel):
    """Single position in `order.items` for table/delivery create."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    product_id: str = Field(alias="productId")
    amount: float
    type: Literal["Product", "Compound"] | None = Field(default=None, alias="type")
    product_size_id: str | None = Field(default=None, alias="productSizeId")
    modifiers: list[OrderCreateModifier] | None = None
    comment: str | None = None


class OrderCreateGuests(BaseModel):
    """Guest count block (`order.guests` in API examples)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int


class OrderCreateOrderPayload(BaseModel):
    """Nested `order` object in the request body."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    table_ids: list[str] | None = Field(default=None, alias="tableIds")
    items: list[OrderCreateItem] | None = None
    guests: OrderCreateGuests | None = None
    comment: str | None = None
    external_number: str | None = Field(default=None, alias="externalNumber")
    phone: str | None = None


class OrderCreateBody(BaseModel):
    """Full JSON body for `POST /api/1/order/create`."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    organization_id: str = Field(alias="organizationId")
    terminal_group_id: str = Field(alias="terminalGroupId")
    order: OrderCreateOrderPayload


class OrderCreateResponse(BaseResponseModel):
    """Response from `POST /api/1/order/create`."""

    model_config = ConfigDict(populate_by_name=True)

    class OrderInfo(BaseModel):
        model_config = ConfigDict(extra="allow", populate_by_name=True)

        id: str
        external_number: str | None = Field(default=None, alias="externalNumber")
        organization_id: str = Field(alias="organizationId")
        timestamp: int
        creation_status: str = Field(alias="creationStatus")
        error_info: Any = Field(default=None, alias="errorInfo")
        order: dict[str, Any]

    order_info: OrderInfo = Field(alias="orderInfo")


class Orders:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def create(
        self,
        organization_id: str,
        terminal_group_id: str,
        order: OrderCreateOrderPayload | Mapping[str, Any],
        timeout: str | int | None = None,
    ) -> OrderCreateResponse:
        """Create a table/restaurant order (Transport).

        Args:
            organization_id: Organization id (from `/api/1/organizations`).
            terminal_group_id: Terminal group id (from `/api/1/terminal_groups`).
            order: Order payload (`tableIds`, `items`, `guests`, etc.). Unknown JSON
                keys are preserved when built via `OrderCreateOrderPayload.model_validate`.
            timeout: Optional request timeout header value (seconds).

        Ref: https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1create/post
        """
        order_payload = OrderCreateOrderPayload.model_validate(dict(order)) if isinstance(order, Mapping) else order
        body = OrderCreateBody.model_validate(
            {
                "organizationId": organization_id,
                "terminalGroupId": terminal_group_id,
                "order": order_payload.model_dump(by_alias=True, exclude_none=True),
            }
        )
        payload = body.model_dump(by_alias=True, exclude_none=True)
        response = await self._client.request("/api/1/order/create", data=payload, timeout=timeout)
        return OrderCreateResponse(**orjson.loads(response.content))

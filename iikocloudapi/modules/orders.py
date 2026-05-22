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


class OrderPaymentAdditionalData(BaseModel):
    """Optional acquiring/loyalty metadata attached to a payment line."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type: str | None = None
    credentials: str | None = None
    search_scope: str | None = Field(default=None, alias="searchScope")


class OrderPaymentItem(BaseModel):
    """Payment line for `order.payments[]` (create) and `change_payments`.

    `paymentTypeKind` is an enum from `/api/1/payment_types`. For T-Bank
    (acquiring done outside iiko) use `External` with `isProcessedExternally=true`
    and put the T-Bank PaymentId into `paymentAdditionalData.credentials`.

    `paymentTypeId` is required by iiko (UUID from `/api/1/payment_types`).
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    payment_type_kind: Literal[
        "Cash", "Card", "Credit", "Writeoff", "Voucher", "External", "IikoCard"
    ] = Field(alias="paymentTypeKind")
    sum: float
    payment_type_id: str = Field(alias="paymentTypeId")
    is_processed_externally: bool | None = Field(default=None, alias="isProcessedExternally")
    payment_additional_data: OrderPaymentAdditionalData | None = Field(
        default=None, alias="paymentAdditionalData"
    )
    is_fiscalized_externally: bool | None = Field(default=None, alias="isFiscalizedExternally")
    is_prepay: bool | None = Field(default=None, alias="isPrepay")


class OrderTipItem(BaseModel):
    """Tip line for `order.tips[]` and `change_payments.tips[]`."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    payment_type_kind: Literal[
        "Cash", "Card", "Credit", "Writeoff", "Voucher", "External", "IikoCard"
    ] = Field(alias="paymentTypeKind")
    tips_type_id: str | None = Field(default=None, alias="tipsTypeId")
    payment_type_id: str = Field(alias="paymentTypeId")
    sum: float
    is_processed_externally: bool | None = Field(default=None, alias="isProcessedExternally")
    payment_additional_data: OrderPaymentAdditionalData | None = Field(
        default=None, alias="paymentAdditionalData"
    )
    is_fiscalized_externally: bool | None = Field(default=None, alias="isFiscalizedExternally")
    is_prepay: bool | None = Field(default=None, alias="isPrepay")


class OrderCreateOrderPayload(BaseModel):
    """Nested `order` object in the request body."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    table_ids: list[str] | None = Field(default=None, alias="tableIds")
    items: list[OrderCreateItem] | None = None
    guests: OrderCreateGuests | None = None
    comment: str | None = None
    external_number: str | None = Field(default=None, alias="externalNumber")
    phone: str | None = None
    payments: list[OrderPaymentItem] | None = None
    tips: list[OrderTipItem] | None = None


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


class OrderCloseBody(BaseModel):
    """Body for `POST /api/1/order/close`."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    organization_id: str = Field(alias="organizationId")
    order_id: str = Field(alias="orderId")
    cheque_additional_info: dict[str, Any] | None = Field(
        default=None, alias="chequeAdditionalInfo"
    )


class OrderCloseResponse(BaseResponseModel):
    """iiko returns just `correlationId` for async close.

    Track completion via `/api/1/commands/status`.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class OrderChangePaymentsBody(BaseModel):
    """Body for `POST /api/1/order/change_payments`."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    organization_id: str = Field(alias="organizationId")
    order_id: str = Field(alias="orderId")
    revision: int | None = None
    payments: list[OrderPaymentItem]
    tips: list[OrderTipItem] | None = None


class OrderChangePaymentsResponse(BaseResponseModel):
    """`change_payments` is async — returns `correlationId`."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class OrderAddItemsBody(BaseModel):
    """Body for `POST /api/1/order/add_items`."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    organization_id: str = Field(alias="organizationId")
    order_id: str = Field(alias="orderId")
    items: list[OrderCreateItem]
    combos: list[dict[str, Any]] | None = None


class OrderAddItemsResponse(BaseResponseModel):
    """`add_items` is async — returns `correlationId`."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class OrderByIdBody(BaseModel):
    """Body for `POST /api/1/order/by_id`."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    organization_ids: list[str] = Field(alias="organizationIds")
    order_ids: list[str] = Field(alias="orderIds")
    source_keys: list[str] | None = Field(default=None, alias="sourceKeys")


class OrderByTableBody(BaseModel):
    """Body for `POST /api/1/order/by_table`."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    organization_ids: list[str] = Field(alias="organizationIds")
    table_ids: list[str] = Field(alias="tableIds")
    source_keys: list[str] | None = Field(default=None, alias="sourceKeys")
    statuses: list[Literal["New", "Bill", "Closed", "Deleted"]] | None = None
    date_from: str | None = Field(default=None, alias="dateFrom")
    date_to: str | None = Field(default=None, alias="dateTo")


class OrderQueryResponse(BaseResponseModel):
    """Common shape for `by_id` / `by_table` — keep `orders` as raw dicts.

    The on-the-wire schema is large (items, payments, history, customer, etc.).
    Callers that need typed access can post-process; we don't lose data.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    orders: list[dict[str, Any]] = Field(default_factory=list)


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
            order: Order payload (`tableIds`, `items`, `guests`, `payments`, etc.).
                Pass `payments` to make the order arrive already paid (pay-first flow).
            timeout: Optional request timeout header value (seconds).

        Ref: https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1create/post
        """
        order_payload = (
            OrderCreateOrderPayload.model_validate(dict(order)) if isinstance(order, Mapping) else order
        )
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

    async def close(
        self,
        organization_id: str,
        order_id: str,
        cheque_additional_info: Mapping[str, Any] | None = None,
        timeout: str | int | None = None,
    ) -> OrderCloseResponse:
        """Close an open table order. Async on iiko side: poll `/api/1/commands/status` with the returned `correlationId`.

        Note: closing does NOT add payment. Call `change_payments` first if the order is not fully paid.

        Ref: https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1close/post
        """
        body = OrderCloseBody.model_validate(
            {
                "organizationId": organization_id,
                "orderId": order_id,
                "chequeAdditionalInfo": dict(cheque_additional_info) if cheque_additional_info else None,
            }
        )
        payload = body.model_dump(by_alias=True, exclude_none=True)
        response = await self._client.request("/api/1/order/close", data=payload, timeout=timeout)
        return OrderCloseResponse(**orjson.loads(response.content))

    async def change_payments(
        self,
        organization_id: str,
        order_id: str,
        payments: list[OrderPaymentItem | Mapping[str, Any]],
        revision: int | None = None,
        tips: list[OrderTipItem | Mapping[str, Any]] | None = None,
        timeout: str | int | None = None,
    ) -> OrderChangePaymentsResponse:
        """Replace `payments` (and optionally `tips`) on an existing open order. Async — track via `correlationId`.

        Use this in cook-first flow after the T-Bank Confirm succeeds: attach an External payment that
        references the T-Bank PaymentId, then call `close`.

        Ref: https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1change_payments/post
        """
        norm_payments = [
            p if isinstance(p, OrderPaymentItem) else OrderPaymentItem.model_validate(dict(p))
            for p in payments
        ]
        norm_tips = (
            [t if isinstance(t, OrderTipItem) else OrderTipItem.model_validate(dict(t)) for t in tips]
            if tips
            else None
        )
        body = OrderChangePaymentsBody.model_validate(
            {
                "organizationId": organization_id,
                "orderId": order_id,
                "revision": revision,
                "payments": [p.model_dump(by_alias=True, exclude_none=True) for p in norm_payments],
                "tips": [t.model_dump(by_alias=True, exclude_none=True) for t in norm_tips] if norm_tips else None,
            }
        )
        payload = body.model_dump(by_alias=True, exclude_none=True)
        response = await self._client.request("/api/1/order/change_payments", data=payload, timeout=timeout)
        return OrderChangePaymentsResponse(**orjson.loads(response.content))

    async def add_items(
        self,
        organization_id: str,
        order_id: str,
        items: list[OrderCreateItem | Mapping[str, Any]],
        combos: list[Mapping[str, Any]] | None = None,
        timeout: str | int | None = None,
    ) -> OrderAddItemsResponse:
        """Append items to an open table order. Async — track via `correlationId`.

        Ref: https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1add_items/post
        """
        norm_items = [
            it if isinstance(it, OrderCreateItem) else OrderCreateItem.model_validate(dict(it))
            for it in items
        ]
        body = OrderAddItemsBody.model_validate(
            {
                "organizationId": organization_id,
                "orderId": order_id,
                "items": [it.model_dump(by_alias=True, exclude_none=True) for it in norm_items],
                "combos": [dict(c) for c in combos] if combos else None,
            }
        )
        payload = body.model_dump(by_alias=True, exclude_none=True)
        response = await self._client.request("/api/1/order/add_items", data=payload, timeout=timeout)
        return OrderAddItemsResponse(**orjson.loads(response.content))

    async def by_id(
        self,
        organization_ids: list[str],
        order_ids: list[str],
        source_keys: list[str] | None = None,
        timeout: str | int | None = None,
    ) -> OrderQueryResponse:
        """Get full order documents by id.

        Ref: https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1by_id/post
        """
        body = OrderByIdBody.model_validate(
            {
                "organizationIds": organization_ids,
                "orderIds": order_ids,
                "sourceKeys": source_keys,
            }
        )
        payload = body.model_dump(by_alias=True, exclude_none=True)
        response = await self._client.request("/api/1/order/by_id", data=payload, timeout=timeout)
        return OrderQueryResponse(**orjson.loads(response.content))

    async def by_table(
        self,
        organization_ids: list[str],
        table_ids: list[str],
        source_keys: list[str] | None = None,
        statuses: list[Literal["New", "Bill", "Closed", "Deleted"]] | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        timeout: str | int | None = None,
    ) -> OrderQueryResponse:
        """List orders open on the given table(s).

        Useful for cook-first flow when the guest re-scans the QR mid-meal: instead of creating
        a second order, find the still-open one and call `add_items`.

        Ref: https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1by_table/post
        """
        body = OrderByTableBody.model_validate(
            {
                "organizationIds": organization_ids,
                "tableIds": table_ids,
                "sourceKeys": source_keys,
                "statuses": statuses,
                "dateFrom": date_from,
                "dateTo": date_to,
            }
        )
        payload = body.model_dump(by_alias=True, exclude_none=True)
        response = await self._client.request("/api/1/order/by_table", data=payload, timeout=timeout)
        return OrderQueryResponse(**orjson.loads(response.content))

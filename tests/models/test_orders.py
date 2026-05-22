import orjson

from iikocloudapi.modules.orders import (
    OrderAddItemsBody,
    OrderByIdBody,
    OrderByTableBody,
    OrderChangePaymentsBody,
    OrderCloseBody,
    OrderCloseResponse,
    OrderCreateBody,
    OrderCreateItem,
    OrderCreateOrderPayload,
    OrderCreateResponse,
    OrderPaymentItem,
    OrderQueryResponse,
)

order_create_response_json = """{
  "correlationId": "11111111-2222-3333-4444-555555555555",
  "orderInfo": {
    "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "externalNumber": "42",
    "organizationId": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": 1700000000,
    "creationStatus": "Success",
    "errorInfo": null,
    "order": {
      "tableIds": ["770e8400-e29b-41d4-a716-446655440099"],
      "customer": null,
      "phone": "",
      "status": "New",
      "sum": 199.5,
      "number": 7,
      "items": [],
      "terminalGroupId": "660e8400-e29b-41d4-a716-446655440001",
      "comment": null
    }
  }
}"""


def test_order_create_response_parses():
    parsed = OrderCreateResponse(**orjson.loads(order_create_response_json))
    assert parsed.correlation_id == "11111111-2222-3333-4444-555555555555"
    assert parsed.order_info.id == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    assert parsed.order_info.creation_status == "Success"
    assert parsed.order_info.order["sum"] == 199.5
    assert parsed.order_info.order["number"] == 7


def test_order_create_body_serializes_and_keeps_extra_on_order():
    body = OrderCreateBody(
        organization_id="550e8400-e29b-41d4-a716-446655440000",
        terminal_group_id="660e8400-e29b-41d4-a716-446655440001",
        order=OrderCreateOrderPayload.model_validate(
            {
                "tableIds": ["770e8400-e29b-41d4-a716-446655440099"],
                "items": [
                    {"productId": "880e8400-e29b-41d4-a716-446655440012", "amount": 2},
                    {
                        "productId": "990e8400-e29b-41d4-a716-446655440013",
                        "amount": 1,
                        "type": "Product",
                        "modifiers": [{"productId": "aa0e8400-e29b-41d4-a716-446655440014", "amount": 1}],
                    },
                ],
                "guestsInfo": {"count": 1, "splitBetweenPersons": False},
                "guests": {"count": 2},
            }
        ),
    )
    dumped = body.model_dump(by_alias=True, exclude_none=True)
    assert dumped["organizationId"] == "550e8400-e29b-41d4-a716-446655440000"
    assert dumped["terminalGroupId"] == "660e8400-e29b-41d4-a716-446655440001"
    assert dumped["order"]["tableIds"] == ["770e8400-e29b-41d4-a716-446655440099"]
    assert dumped["order"]["guestsInfo"]["count"] == 1
    assert dumped["order"]["guestsInfo"]["splitBetweenPersons"] is False
    assert dumped["order"]["guests"]["count"] == 2
    assert len(dumped["order"]["items"]) == 2
    assert dumped["order"]["items"][1]["modifiers"][0]["productId"] == "aa0e8400-e29b-41d4-a716-446655440014"


def test_order_create_item_optional_type_omitted_from_payload_when_none():
    body = OrderCreateBody(
        organization_id="org",
        terminal_group_id="tg",
        order=OrderCreateOrderPayload(
            items=[OrderCreateItem(product_id="pid", amount=1.0)],
        ),
    )
    dumped = body.model_dump(by_alias=True, exclude_none=True)
    assert "type" not in dumped["order"]["items"][0]


def test_order_create_with_external_payment_pay_first():
    """Pay-first flow: order arrives already paid via external acquiring (e.g. T-Bank)."""
    body = OrderCreateBody(
        organization_id="org",
        terminal_group_id="tg",
        order=OrderCreateOrderPayload.model_validate(
            {
                "tableIds": ["table-uuid"],
                "items": [{"productId": "pid", "amount": 1, "type": "Product"}],
                "payments": [
                    {
                        "paymentTypeKind": "External",
                        "sum": 199.5,
                        "paymentTypeId": "external-payment-type-uuid",
                        "isProcessedExternally": True,
                        "paymentAdditionalData": {
                            "credentials": "tbank-payment-id-123",
                            "type": "TBank",
                        },
                        "isFiscalizedExternally": False,
                    }
                ],
            }
        ),
    )
    dumped = body.model_dump(by_alias=True, exclude_none=True)
    payment = dumped["order"]["payments"][0]
    assert payment["paymentTypeKind"] == "External"
    assert payment["isProcessedExternally"] is True
    assert payment["paymentAdditionalData"]["credentials"] == "tbank-payment-id-123"
    assert payment["sum"] == 199.5


def test_order_close_body_minimal():
    body = OrderCloseBody(organization_id="org", order_id="ord")
    dumped = body.model_dump(by_alias=True, exclude_none=True)
    assert dumped == {"organizationId": "org", "orderId": "ord"}


def test_order_close_body_with_cheque_info():
    body = OrderCloseBody.model_validate(
        {
            "organizationId": "org",
            "orderId": "ord",
            "chequeAdditionalInfo": {"email": "guest@example.com"},
        }
    )
    dumped = body.model_dump(by_alias=True, exclude_none=True)
    assert dumped["chequeAdditionalInfo"]["email"] == "guest@example.com"


def test_order_close_response_parses_minimal():
    parsed = OrderCloseResponse(**orjson.loads('{"correlationId": "corr-1"}'))
    assert parsed.correlation_id == "corr-1"


def test_order_change_payments_body_serializes_payments_list():
    body = OrderChangePaymentsBody(
        organization_id="org",
        order_id="ord",
        revision=12,
        payments=[
            OrderPaymentItem(
                payment_type_kind="External",
                sum=500.0,
                payment_type_id="ext-pt",
                is_processed_externally=True,
            )
        ],
    )
    dumped = body.model_dump(by_alias=True, exclude_none=True)
    assert dumped["revision"] == 12
    assert dumped["payments"][0]["paymentTypeKind"] == "External"
    assert dumped["payments"][0]["isProcessedExternally"] is True
    assert dumped["payments"][0]["sum"] == 500.0


def test_order_add_items_body_round_trips_items():
    body = OrderAddItemsBody.model_validate(
        {
            "organizationId": "org",
            "orderId": "ord",
            "items": [{"productId": "pid", "amount": 2, "type": "Product"}],
        }
    )
    dumped = body.model_dump(by_alias=True, exclude_none=True)
    assert dumped["items"][0]["productId"] == "pid"
    assert dumped["items"][0]["amount"] == 2
    assert dumped["items"][0]["type"] == "Product"


def test_order_by_id_body_serializes():
    body = OrderByIdBody.model_validate(
        {"organizationIds": ["o1"], "orderIds": ["ord1", "ord2"]}
    )
    dumped = body.model_dump(by_alias=True, exclude_none=True)
    assert dumped == {"organizationIds": ["o1"], "orderIds": ["ord1", "ord2"]}


def test_order_by_table_body_with_statuses_filter():
    body = OrderByTableBody.model_validate(
        {
            "organizationIds": ["o1"],
            "tableIds": ["t1"],
            "statuses": ["New", "Bill"],
        }
    )
    dumped = body.model_dump(by_alias=True, exclude_none=True)
    assert dumped["statuses"] == ["New", "Bill"]


def test_order_query_response_keeps_orders_as_dicts():
    payload = """{
      "correlationId": "c",
      "orders": [
        {"id": "ord-1", "status": "New", "sum": 100, "payments": []}
      ]
    }"""
    parsed = OrderQueryResponse(**orjson.loads(payload))
    assert parsed.orders[0]["id"] == "ord-1"
    assert parsed.orders[0]["status"] == "New"

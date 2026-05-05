import orjson

from iikocloudapi.modules.orders import (
    OrderCreateBody,
    OrderCreateItem,
    OrderCreateOrderPayload,
    OrderCreateResponse,
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

import orjson

from iikocloudapi.modules.dictionaries import (
    CancelCausesResponse,
    DiscountsResponse,
    OrderTypesResponse,
    PaymentTypesResponse,
    RemovalTypesResponse,
    TipsTypesResponse,
)

cancel_causes_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "cancelCauses": [
    {
      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
      "name": "string",
      "isDeleted": true
    }
  ]
}"""

order_types_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "orderTypes": [
    {
      "organizationId": "7bc05553-4b68-44e8-b7bc-37be63c6d9e9",
      "items": [
        {
          "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
          "name": "string",
          "orderServiceType": "Common",
          "isDeleted": true,
          "externalRevision": 0,
          "isDefault": true
        }
      ]
    }
  ]
}"""

discounts_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "discounts": [
    {
      "organizationId": "7bc05553-4b68-44e8-b7bc-37be63c6d9e9",
      "items": [
        {
          "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
          "name": "string",
          "percent": 0,
          "isCategorisedDiscount": true,
          "productCategoryDiscounts": [
            {
              "categoryId": "337f5e5d-288b-40d5-be14-901cc3acacc0",
              "categoryName": "string",
              "percent": 0
            }
          ],
          "comment": "string",
          "canBeAppliedSelectively": true,
          "minOrderSum": 0,
          "mode": "Percent",
          "sum": 0,
          "canApplyByCardNumber": true,
          "isManual": true,
          "isCard": true,
          "isAutomatic": true,
          "isDeleted": true
        }
      ]
    }
  ]
}"""


payment_types_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "paymentTypes": [
    {
      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
      "code": "string",
      "name": "string",
      "comment": "string",
      "combinable": true,
      "externalRevision": 0,
      "applicableMarketingCampaigns": [
        "497f6eca-6276-4993-bfeb-53cbbbba6f08"
      ],
      "isDeleted": true,
      "printCheque": true,
      "paymentProcessingType": "External",
      "paymentTypeKind": "Unknown",
      "terminalGroups": [
        {
          "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
          "organizationId": "7bc05553-4b68-44e8-b7bc-37be63c6d9e9",
          "name": "string",
          "address": "string",
          "timeZone": "string",
          "externalData": [
            {
              "key": "string",
              "value": "string"
            }
          ]
        }
      ]
    }
  ]
}"""

removal_types_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "removalTypes": [
    {
      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
      "name": "string",
      "comment": "string",
      "canWriteoffToCafe": true,
      "canWriteoffToWaiter": true,
      "canWriteoffToUser": true,
      "reasonRequired": true,
      "manual": true,
      "isDeleted": true
    }
  ]
}"""

tips_types_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "tipsTypes": [
    {
      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
      "name": "string",
      "organizationIds": [
        "497f6eca-6276-4993-bfeb-53cbbbba6f08"
      ],
      "orderServiceTypes": [
        "Common"
      ],
      "paymentTypesIds": [
        "497f6eca-6276-4993-bfeb-53cbbbba6f08"
      ]
    }
  ]
}"""


def test_cancel_causes_model():
    CancelCausesResponse(**orjson.loads(cancel_causes_json))


def test_order_types_model():
    OrderTypesResponse(**orjson.loads(order_types_json))


def test_discounts_model():
    DiscountsResponse(**orjson.loads(discounts_json))


def test_payment_types_model():
    PaymentTypesResponse(**orjson.loads(payment_types_json))


def test_removal_types_model():
    RemovalTypesResponse(**orjson.loads(removal_types_json))


def test_tips_types_model():
    TipsTypesResponse(**orjson.loads(tips_types_json))

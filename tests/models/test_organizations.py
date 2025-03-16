import orjson

from iikocloudapi.modules.organizations import (
    OrganizationsResponse,
    OrganizationsSettingsResponse,
    OrganizationExtendedModel,
    OrganizationSimpleModel,
)

available_organizations_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "organizations": [
    {
      "responseType": "Simple",
      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
      "name": "string",
      "code": "string",
      "externalData": [
        {
          "key": "string",
          "value": "string"
        }
      ]
    }
  ]
}"""


available_organizations_with_additional_info_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "organizations": [
    {
      "responseType": "Simple",
      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
      "name": "string",
      "code": "string",
      "latitude": 0,
      "longitude": 0,
      "useUaeAddressingSystem": false,
      "version": "1.0.0",
      "addressFormatType": "City",
      "isCloud": true,
      "isAnonymousGuestsAllowed": true,
      "addressLookup": ["DaData"],
      "externalData": [
        {
          "key": "string",
          "value": "string"
        }
      ]
    }
  ]
}"""


def test_organizations_model():
    m = OrganizationsResponse(**orjson.loads(available_organizations_json))
    assert isinstance(m.organizations[0], OrganizationSimpleModel)


def test_organizations_response_with_additional_info():
    m = OrganizationsResponse(
        **orjson.loads(available_organizations_with_additional_info_json)
    )
    assert isinstance(m.organizations[0], OrganizationExtendedModel)


def test_organizations_settings_response():
    OrganizationsSettingsResponse(
        **orjson.loads(available_organizations_json)
    )

import orjson

from iikocloudapi.modules.terminal_groups import (
    TerminalAwakeResponse,
    TerminalGroupsResponse,
    TerminalIsAliveResponse,
)

terminal_groups_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "terminalGroups": [
    {
      "organizationId": "7bc05553-4b68-44e8-b7bc-37be63c6d9e9",
      "items": [
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
  ],
  "terminalGroupsInSleep": [
    {
      "organizationId": "7bc05553-4b68-44e8-b7bc-37be63c6d9e9",
      "items": [
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

terminal_groups_is_alive_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "isAliveStatus": [
    {
      "isAlive": true,
      "terminalGroupId": "4fab19a5-203c-4bf5-94eb-f572aa8b117b",
      "organizationId": "7bc05553-4b68-44e8-b7bc-37be63c6d9e9"
    }
  ]
}
"""

terminal_groups_awake_json = """{
  "successfullyProcessed": [
    "497f6eca-6276-4993-bfeb-53cbbbba6f08"
  ],
  "failedProcessed": [
    "497f6eca-6276-4993-bfeb-53cbbbba6f08"
  ]
}"""


def test_terminal_groups_model():
    TerminalGroupsResponse(**orjson.loads(terminal_groups_json))


def test_terminal_groups_is_alive_model():
    TerminalIsAliveResponse(**orjson.loads(terminal_groups_is_alive_json))


def test_terminal_groups_awake_model():
    TerminalAwakeResponse(**orjson.loads(terminal_groups_awake_json))

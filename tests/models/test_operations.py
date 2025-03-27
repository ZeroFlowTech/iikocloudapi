import orjson

from iikocloudapi.modules.operations import CommandsStatusResponse

command_status_json = """{
  "state": "InProgress"
}"""


def test_command_status_response():
    CommandsStatusResponse(**orjson.loads(command_status_json))

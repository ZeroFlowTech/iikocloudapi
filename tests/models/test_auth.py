import orjson

from iikocloudapi.client import AccessTokenResponse

access_token_json = """{
  "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
  "token": "string"
}"""


def test_access_token_response():
    AccessTokenResponse(**orjson.loads(access_token_json))

import orjson

from iikocloudapi.modules.notifications import SendResponse

send_notification_json = """{
    "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c"
}"""


def test_send_model():
    SendResponse(**orjson.loads(send_notification_json))

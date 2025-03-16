from iikocloudapi.client import Client
from iikocloudapi.modules.notifications import Notifications
from iikocloudapi.modules.organizations import Organizations


class iikoCloudApi:
    def __init__(self, client: Client) -> None:
        self._client = client

        self.notifications = Notifications(self._client)
        self.organizations = Organizations(self._client)

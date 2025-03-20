from iikocloudapi.client import Client
from iikocloudapi.modules.auth import Auth
from iikocloudapi.modules.dictionaries import Dictionaries
from iikocloudapi.modules.menu import Menu
from iikocloudapi.modules.notifications import Notifications
from iikocloudapi.modules.organizations import Organizations


class iikoCloudApi:
    def __init__(self, client: Client) -> None:
        self._client = client

        self.auth = Auth(self._client)
        self.notifications = Notifications(self._client)
        self.organizations = Organizations(self._client)
        self.dictionaries = Dictionaries(self._client)
        self.menu = Menu(self._client)

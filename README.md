# iikoCloud API client

## Установка

```
pip install iikocloudapi
```

## Как работает

Примеры запросов и названия методов:
- /api/1/notifications/send - `iiko_client.notifications.send(...)`
- /api/1/organizations - `iiko_client.organizations(...)`
- /api/1/organizations/settings - `iiko_client.organizations.settings(...)`


## Пример использования

```
import asyncio

from iikocloudapi import Client, iikoCloudApi

iiko_client = iikoCloudApi(Client("xxxxx"))


async def main():
    await iiko_client.organizations()


if __name__ == "__main__":
    asyncio.run(main())
```

## Реализованные методы
- Authorization
    - [x] [Retrieve session key for API user.](https://api-ru.iiko.services/#tag/Authorization/paths/~1api~11~1access_token/post)
- Notifications
    - [x] [Send notification to external systems (iikoFront and iikoWeb).](https://api-ru.iiko.services/#tag/Notifications/paths/~1api~11~1notifications~1send/post)
- Organizations
    - [x] [Returns organizations available to api-login user.](https://api-ru.iiko.services/#tag/Organizations/paths/~1api~11~1organizations/post)
    - [x] [Returns available to api-login user organizations specified settings.](https://api-ru.iiko.services/#tag/Organizations/paths/~1api~11~1organizations~1settings/post)

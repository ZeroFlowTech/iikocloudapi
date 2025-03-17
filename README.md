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

[Документация iikoCloud API](https://github.com/ZeroFlowTech)

- [Authorization](https://api-ru.iiko.services/#tag/Authorization)
    - [x] [Retrieve session key for API user.](https://api-ru.iiko.services/#tag/Authorization/paths/~1api~11~1access_token/post)
- [Notifications](https://api-ru.iiko.services/#tag/Notifications)
    - [x] [Send notification to external systems (iikoFront and iikoWeb).](https://api-ru.iiko.services/#tag/Notifications/paths/~1api~11~1notifications~1send/post)
- [Organizations](https://api-ru.iiko.services/#tag/Organizations)
    - [x] [Returns organizations available to api-login user.](https://api-ru.iiko.services/#tag/Organizations/paths/~1api~11~1organizations/post)
    - [x] [Returns available to api-login user organizations specified settings.](https://api-ru.iiko.services/#tag/Organizations/paths/~1api~11~1organizations~1settings/post)
- [Terminal groups](https://api-ru.iiko.services/#tag/Terminal-groups)
    - [x] [Method that returns information on groups of delivery terminals.](https://api-ru.iiko.services/#tag/Terminal-groups/paths/~1api~11~1terminal_groups/post)
    - [x] [Returns information on availability of group of terminals.](https://api-ru.iiko.services/#tag/Terminal-groups/paths/~1api~11~1terminal_groups~1is_alive/post)
    - [x] [Awake terminal groups from sleep mode.](https://api-ru.iiko.services/#tag/Terminal-groups/paths/~1api~11~1terminal_groups~1awake/post)
- [Dictionaries](https://api-ru.iiko.services/#tag/Dictionaries)
    - [x] [Delivery cancel causes.](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1cancel_causes/post)
    - [x] [Order types.](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1deliveries~1order_types/post)
    - [x] [Discounts / surcharges.](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1discounts/post)
    - [x] [Payment types.](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1payment_types/post)
    - [x] [Removal types (reasons for deletion).](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1removal_types/post)
    - [x] [Get tips types for api-login`s rms group.](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1tips_types/post)

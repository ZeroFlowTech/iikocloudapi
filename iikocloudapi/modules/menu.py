import enum
from decimal import Decimal
from typing import Literal

import orjson
from pydantic import BaseModel, Field

from iikocloudapi.client import Client
from iikocloudapi.helpers import BaseResponseModel


class MenuResponse(BaseResponseModel):
    class Item(BaseModel):
        id: str
        name: str

    external_menus: list[Item] = Field(alias="externalMenus")
    price_categories: list[Item] = Field(alias="priceCategories")


class AllergenGroup(BaseModel):
    id: str
    code: str
    name: str


class Price(BaseModel):
    organization_id: str = Field(alias="organizationId")
    price: float


class Restriction(BaseModel):
    min_quantity: int = Field(alias="minQuantity")
    max_quantity: int = Field(alias="maxQuantity")
    free_quantity: int = Field(alias="freeQuantity")
    by_default: int = Field(alias="byDefault")


class Tag(BaseModel):
    id: str
    name: str


class MenuByIdResponse(BaseModel):
    class ItemCategory(BaseModel):
        class Item(BaseModel):
            class TaxCategory(BaseModel):
                id: str
                name: str
                percentage: float

            class ItemSize(BaseModel):
                class ItemModifierGroup(BaseModel):
                    class Item(BaseModel):
                        sku: str
                        name: str
                        description: str
                        button_image: str = Field(alias="buttonImage")
                        item_id: str = Field(alias="itemId")
                        nutrition_per_hundred_grams: dict = Field(alias="nutritionPerHundredGrams")
                        portion_weight_grams: float = Field(alias="portionWeightGrams")
                        tags: list[Tag]
                        prices: list[Price]
                        restrictions: Restriction
                        allergen_groups: list[AllergenGroup] = Field([], alias="allergenGroups")

                    sku: str
                    name: str
                    description: str
                    can_be_divided: bool = Field(alias="canBeDivided")
                    item_group_id: str = Field(alias="itemGroupId")
                    child_modifiers_have_min_max_restrictions: bool = Field(
                        alias="childModifiersHaveMinMaxRestrictions"
                    )
                    restrictions: Restriction

                sku: str
                size_code: str = Field(alias="sizeCode")
                size_name: str = Field(alias="sizeName")
                is_default: bool = Field(alias="isDefault")
                portion_weight_grams: float = Field(alias="portionWeightGrams")
                size_id: str | None = Field(None, alias="sizeId")
                nutrition_per_hundred_grams: dict = Field(alias="nutritionPerHundredGrams")
                button_image_url: str | None = Field(None, alias="buttonImageUrl")
                button_image_cropped_url: list[str] = Field([], alias="buttonImageCroppedUrl")
                prices: list[Price]
                item_modifier_groups: list[ItemModifierGroup] = Field(alias="itemModifierGroups")

            sku: str
            name: str
            description: str
            item_id: str = Field(alias="itemId")
            modifier_schema_id: str | None = Field(None, alias="modifierSchemaId")
            order_item_type: Literal["Product", "Compound"] = Field(alias="orderItemType")
            allergen_groups: list[AllergenGroup] = Field([], alias="allergenGroups")
            tax_category: TaxCategory | None = Field(None, alias="taxCategory")
            item_sizes: list[ItemSize] = Field(alias="itemSizes")

        id: str
        name: str
        description: str
        items: list[Item]
        button_image_url: str | None = Field(None, alias="buttonImageUrl")
        header_image_url: str | None = Field(None, alias="headerImageUrl")

    id: int
    name: str
    description: str
    item_categories: list[ItemCategory] = Field(alias="itemCategories")


class StopListsResponse(BaseResponseModel):
    class TerminalGroupStopList(BaseModel):
        class Item(BaseModel):
            class Item(BaseModel):
                balance: Decimal
                product_id: str = Field(alias="productId")
                sku: str | None = None
                size_id: str | None = Field(None, alias="sizeId")
                date_add: str | None = Field(None, alias="dateAdd")

            terminal_group_id: str = Field(alias="terminalGroupId")
            items: list[Item]

        organization_id: str = Field(alias="organizationId")
        items: list[Item]

    terminal_group_stop_lists: list[TerminalGroupStopList] = Field(alias="terminalGroupStopLists")


class StopListsCheckResponse(BaseResponseModel):
    class RejectedItem(BaseModel):
        balance: Decimal
        product_id: str = Field(alias="productId")
        size_id: str | None = Field(alias="sizeId")
        sku: str | None = None
        date_add: str | None = Field(None, alias="dateAdd")

    rejected_items: list[RejectedItem] = Field(alias="rejectedItems")


class Product(BaseModel):
    # TODO: Add fields from https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1stop_lists~1check/post
    pass


class Compound(BaseModel):
    # TODO: Add fields from https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1stop_lists~1check/post
    pass


class ItemStopListAdd(BaseModel):
    product_id: str = Field(alias="productId")
    balance: Decimal
    size_id: str | None = Field(None, alias="sizeId")


class ItemStopListRemove(BaseModel):
    product_id: str = Field(alias="productId")
    size_id: str | None = Field(None, alias="sizeId")


class ComboResponse(BaseModel):
    class ComboSpecification(BaseModel):
        class PriceModificationTypeEnum(int, enum.Enum):
            fixed_combo_price = 0
            fixed_position_price = 1
            cheapest_position_discount = 2
            most_expensive_position_discount = 3
            percentage_discount_for_each_position = 4

        class Group(BaseModel):
            class Product(BaseModel):
                product_id: str = Field(alias="productId")
                size_name: str = Field(alias="sizeName")
                size_id: str | None = Field(None, alias="sizeId")
                forbidden_modifiers: list[str] = Field(alias="forbiddenModifiers")
                price_modification_amount: Decimal = Field(alias="priceModificationAmount")

            id: str
            name: str
            is_main_group: bool = Field(alias="isMainGroup")
            products: list[Product]

        source_action_id: str = Field(alias="sourceActionId")
        category_id: str | None = Field(None, alias="categoryId")
        name: str
        price_modification_type: PriceModificationTypeEnum = Field(alias="priceModificationType")
        price_modification: Decimal = Field(alias="priceModification")
        is_active: bool | None = Field(None, alias="isActive")
        start_date: str | None = Field(None, alias="startDate")
        expiration_date: str | None = Field(None, alias="expirationDate")
        lacking_groups_to_suggest: int | None = Field(None, alias="lackingGroupsToSuggest")
        include_modifiers: bool | None = Field(None, alias="includeModifiers")
        groups: list[Group]

    class ComboCategory(BaseModel):
        id: str
        name: str

    class Warnings(BaseModel):
        code: str = Field(alias="Code")
        error_code: str = Field(alias="ErrorCode")
        message: str = Field(alias="Message")

    combo_specifications: list[ComboSpecification] = Field(alias="comboSpecifications")
    combo_categories: list[ComboCategory] = Field(alias="comboCategories")
    warnings: list[Warnings] = Field(alias="Warnings")


class ComboCalculateResponse(BaseModel):
    price: Decimal
    incorrectly_filled_groups: list[str] = Field(alias="incorrectlyFilledGroups")


class Menu:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def __call__(self, timeout: str | int | None = None) -> MenuResponse:
        """External menus with price categories.

        Args:
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Menu/paths/~1api~12~1menu/post
        """
        response = await self._client.request(
            "/api/2/menu",
            timeout=timeout,
        )
        return MenuResponse(**orjson.loads(response.content))

    async def by_id(
        self,
        external_menu_id: str,
        organization_ids: list[str],
        price_category_id: str | None = None,
        version: int | None = None,
        language: str | None = None,
        start_revision: int | None = None,
        timeout: str | int | None = None,
    ) -> MenuByIdResponse:
        """Retrieve external menu by ID.

        Args:
            external_menu_id (str): External menu id
                Can be obtained by `/api/2/menu` operation.
            organization_ids (list[str]): Organization IDs.
                Can be obtained by `/api/1/organizations` operation.
            price_category_id (str | None, optional): Price category id.
                Can be obtained by api/2/menu operation.
                Defaults to None.
            version (int | None, optional): Version of the result data model.
                Defaults to None.
            language (str | None, optional): Language of the external menu.
                Defaults to None.
            start_revision (int | None, optional): Start revision.
                Defaults to None.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Menu/paths/~1api~12~1menu~1by_id/post
        """
        response = await self._client.request(
            "/api/2/menu/by_id",
            data={
                "externalMenuId": external_menu_id,
                "organizationIds": organization_ids,
                "priceCategoryId": price_category_id,
                "version": version,
                "language": language,
                "startRevision": start_revision,
            },
            timeout=timeout,
        )
        return MenuByIdResponse(**orjson.loads(response.content))

    async def stop_lists(
        self,
        organization_ids: list[str],
        return_size: bool = False,
        terminal_groups_ids: list[str] | None = None,
        timeout: str | int | None = None,
    ) -> StopListsResponse:
        """Out-of-stock items.

        Args:
            organization_ids (list[str]): Organizations for which out-of-stock lists will be requested.
                Can be obtained by `/api/1/organizations` operation.
            return_size (bool, optional): Flag indicating the need to return the sizes of the dish.
                Defaults to False.
            terminal_groups_ids (list[str] | None, optional): List of terminal groups
                for which you need to get out-of-stock lists.
                Can be obtained by `/api/1/terminal_groups` operation.
                Defaults to None.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1stop_lists/post
        """
        response = await self._client.request(
            "/api/1/stop_lists",
            data={
                "organizationIds": organization_ids,
                "returnSize": return_size,
                "terminalGroupsIds": terminal_groups_ids,
            },
            timeout=timeout,
        )
        return StopListsResponse(**orjson.loads(response.content))

    async def stop_lists_check(
        self,
        organization_id: str,
        terminal_group_id: str,
        items: list[Product | Compound],
        timeout: str | int | None = None,
    ) -> StopListsCheckResponse:
        """Check items in out-of-stock list.

        Args:
            organization_id (str): Organization ID.
                Can be obtained by `/api/1/organizations` operation.
            terminal_group_id (str): Front group ID the order must be sent to.
                Can be obtained by `/api/1/terminal_groups` operation.
            items (list[Product  |  Compound]): Order items.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1stop_lists~1check/post
        """
        response = await self._client.request(
            "/api/1/stop_lists/check",
            data={
                "organizationId": organization_id,
                "terminalGroupId": terminal_group_id,
                "items": [item.model_dump() for item in items],
            },
            timeout=timeout,
        )
        return StopListsCheckResponse(**orjson.loads(response.content))

    async def stop_lists_add(
        self,
        organization_id: str,
        terminal_group_id: str,
        items: list[ItemStopListAdd],
        timeout: str | int | None = None,
    ) -> BaseResponseModel:
        """Add items to out-of-stock list. (You should have extra rights to use this method).

        Args:
            organization_id (str): Organization ID.
                Can be obtained by `/api/1/organizations` operation.
            terminal_group_id (str): Terminal group ID.
                Can be obtained by `/api/1/terminal_groups` operation.
            items (list[ItemStopListAdd]): Items for adding to out-of-stock list.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1stop_lists~1add/post
        """
        response = await self._client.request(
            "/api/1/stop_lists/add",
            data={
                "organizationId": organization_id,
                "terminalGroupId": terminal_group_id,
                "items": [item.model_dump() for item in items],
            },
            timeout=timeout,
        )
        return BaseResponseModel(**orjson.loads(response.content))

    async def stop_lists_remove(
        self,
        organization_id: str,
        terminal_group_id: str,
        items: list[ItemStopListRemove],
        timeout: str | int | None = None,
    ) -> BaseResponseModel:
        """Remove items from out-of-stock list. (You should have extra rights to use this method).

        Args:
            organization_id (str): Organization ID.
                Can be obtained by `/api/1/organizations` operation.
            terminal_group_id (str): Terminal group ID.
                Can be obtained by `/api/1/terminal_groups` operation.
            items (list[ItemStopListAdd]): Items for removing from out-of-stock list.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1stop_lists~1remove/post
        """
        response = await self._client.request(
            "/api/1/stop_lists/remove",
            data={
                "organizationId": organization_id,
                "terminalGroupId": terminal_group_id,
                "items": [item.model_dump() for item in items],
            },
            timeout=timeout,
        )
        return BaseResponseModel(**orjson.loads(response.content))

    async def stop_lists_clear(
        self,
        organization_id: str,
        terminal_group_id: str,
        timeout: str | int | None = None,
    ) -> BaseResponseModel:
        """Clear out-of-stock list. (You should have extra rights to use this method).

        Args:
            organization_id (str): Organization ID.
                Can be obtained by `/api/1/organizations` operation.
            terminal_group_id (str): Terminal group ID.
                Can be obtained by `/api/1/terminal_groups` operation.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1stop_lists~1clear/post
        """
        response = await self._client.request(
            "/api/1/stop_lists/clear",
            data={
                "organizationId": organization_id,
                "terminalGroupId": terminal_group_id,
            },
            timeout=timeout,
        )
        return BaseResponseModel(**orjson.loads(response.content))

    async def combo(
        self,
        organization_id: str,
        extra_data: bool = False,
        timeout: str | int | None = None,
    ) -> ComboResponse:
        """Get combos info.

        Args:
            organization_id (str): Organization id.
            extra_data (bool, optional): Extra data.
                Defaults to False.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1combo/post
        """
        response = await self._client.request(
            "/api/1/combo",
            data={
                "organizationId": organization_id,
                "extraData": extra_data,
            },
            timeout=timeout,
        )
        return ComboResponse(**orjson.loads(response.content))

    async def combo_calculate(
        self,
        organization_id: str,
        items: list[Product | Compound],
        timeout: str | int | None = None,
    ) -> ComboCalculateResponse:
        """Calculate combo price.

        Args:
            organization_id (str): Organization id.
            items (list[Product  |  Compound]): Items with modifiers included in combo.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1combo~1calculate/post
        """
        response = await self._client.request(
            "/api/1/combo/calculate",
            data={
                "organizationId": organization_id,
                "items": [item.model_dump() for item in items],
            },
            timeout=timeout,
        )
        return ComboCalculateResponse(**orjson.loads(response.content))

    async def nomenclature(
        self,
        organization_id: str,
        start_revision: int | None = None,
        timeout: str | int | None = None,
    ) -> dict:
        """Menu.

        Args:
            organization_id (str): Organization ID.
                Can be obtained by `/api/1/organizations` operation.
            start_revision (int | None, optional): The revision (version) of the menu saved on the integration side.
                Use `0` for the first request for each organization. In every subsequent request,
                the `startRevision` field should contain the value of the `revision` field
                received in the response to the previous request.
                Defaults to None.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1nomenclature/post
        """
        response = await self._client.request(
            "/api/1/nomenclature",
            data={
                "organizationId": organization_id,
                "startRevision": start_revision,
            },
            timeout=timeout,
        )
        return orjson.loads(response.content)

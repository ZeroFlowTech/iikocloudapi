from decimal import Decimal
from typing import Literal

import orjson
from pydantic import BaseModel, Field

from iikocloudapi.client import Client
from iikocloudapi.helpers import BaseResponseModel
from iikocloudapi.modules.terminal_groups import Terminal


class CancelCausesResponse(BaseResponseModel):
    class CancelCause(BaseModel):
        id: str
        name: str
        is_deleted: bool = Field(alias="isDeleted")

    cancel_causes: list[CancelCause] = Field(alias="cancelCauses")


class OrderTypesResponse(BaseResponseModel):
    class OrderTypes(BaseModel):
        class Item(BaseModel):
            id: str
            name: str
            order_service_type: Literal[
                "Common", "DeliveryByCourier", "DeliveryPickUp"
            ] = Field(alias="orderServiceType")
            is_deleted: bool = Field(alias="isDeleted")
            external_revision: int | None = Field(None, alias="externalRevision")
            is_default: bool | None = Field(None, alias="isDefault")

        organization_id: str = Field(alias="organizationId")
        items: list[Item]

    order_types: list[OrderTypes] = Field(alias="orderTypes")


class DiscountsResponse(BaseResponseModel):
    class Discount(BaseModel):
        class Item(BaseModel):
            class ProductCategoryDiscount(BaseModel):
                category_id: str = Field(alias="categoryId")
                category_name: str | None = Field(alias="categoryName")
                percent: Decimal

            id: str
            name: str | None = None
            percent: Decimal
            is_categorised_discount: bool = Field(alias="isCategorisedDiscount")
            product_category_discounts: list[ProductCategoryDiscount] = Field(
                alias="productCategoryDiscounts"
            )
            comment: str | None = None
            can_be_applied_selectively: bool = Field(alias="canBeAppliedSelectively")
            min_order_sum: Decimal | None = Field(alias="minOrderSum")
            mode: Literal["Percent", "FlexibleSum", "FixedSum"]
            sum: Decimal
            can_apply_by_card_number: bool = Field(alias="canApplyByCardNumber")
            is_manual: bool = Field(alias="isManual")
            is_card: bool = Field(alias="isCard")
            is_automatic: bool = Field(alias="isAutomatic")
            is_deleted: bool | None = None

        organization_id: str = Field(alias="organizationId")
        items: list[Item]

    discounts: list[Discount]


class PaymentTypesResponse(BaseResponseModel):
    class PaymentType(BaseModel):
        id: str | None = None
        code: str | None = None
        name: str | None = None
        comment: str | None = None
        combinable: bool
        external_revision: int | None = Field(None, alias="externalRevision")
        applicable_marketing_campaigns: list[str] = Field(
            alias="applicableMarketingCampaigns"
        )
        is_deleted: bool = Field(alias="isDeleted")
        print_cheque: bool = Field(alias="printCheque")
        payment_processing_type: Literal["External", "Internal", "Both"] | None = Field(
            None, alias="paymentProcessingType"
        )
        payment_type_kind: str | None = Field(alias="paymentTypeKind")
        terminal_groups: list[Terminal] = Field(alias="terminalGroups")

    payment_types: list[PaymentType] = Field(alias="paymentTypes")


class RemovalTypesResponse(BaseResponseModel):
    class RemovalType(BaseModel):
        id: str
        name: str
        comment: str | None = None
        can_writeoff_to_cafe: bool = Field(alias="canWriteoffToCafe")
        can_writeoff_to_waiter: bool = Field(alias="canWriteoffToWaiter")
        can_writeoff_to_user: bool = Field(alias="canWriteoffToUser")
        reason_qequired: bool = Field(alias="reasonRequired")
        manual: bool
        is_deleted: bool = Field(alias="isDeleted")

    removal_types: list[RemovalType] = Field(alias="removalTypes")


class TipsTypesResponse(BaseResponseModel):
    class TipType(BaseModel):
        id: str
        name: str
        organization_ids: list[str] = Field(alias="organizationIds")
        order_service_types: list[
            Literal["Common", "DeliveryByCourier", "DeliveryPickUp"]
        ] = Field(alias="orderServiceTypes")
        payment_types_ids: list[str] = Field(alias="paymentTypesIds")

    tips_types: list[TipType] = Field(alias="tipsTypes")


class Dictionaries:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def cancel_causes(
        self,
        organization_ids: list[str],
        timeout: str | int | None = None,
    ) -> CancelCausesResponse:
        """Delivery cancel causes.

        Args:
            organization_ids (list[str]): Organizations ids which delivery cancel causes needs to be returned.
                Can be obtained by `/api/1/organizations` operation.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1cancel_causes/post
        """
        response = await self._client.request(
            "/api/1/cancel_causes",
            data={
                "organizationIds": organization_ids,
            },
            timeout=timeout,
        )
        return CancelCausesResponse(**orjson.loads(response.content))

    async def order_types(
        self,
        organization_ids: list[str],
        timeout: str | int | None = None,
    ) -> OrderTypesResponse:
        """Order types.

        Args:
            organization_ids (list[str]): Organizations IDs which payment types have to be returned.
                Can be obtained by `/api/1/organizations` operation.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1deliveries~1order_types/post
        """
        response = await self._client.request(
            "/api/1/order_types",
            data={
                "organizationIds": organization_ids,
            },
            timeout=timeout,
        )
        return OrderTypesResponse(**orjson.loads(response.content))

    async def discounts(
        self,
        organization_ids: list[str],
        timeout: str | int | None = None,
    ) -> DiscountsResponse:
        """Discounts / surcharges.

        Args:
            organization_ids (list[str]): Organization IDs that require discounts return.
                Can be obtained by `/api/1/organizations` operation.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1discounts/post
        """
        response = await self._client.request(
            "/api/1/discounts",
            data={
                "organizationIds": organization_ids,
            },
            timeout=timeout,
        )
        return DiscountsResponse(**orjson.loads(response.content))

    async def payment_types(
        self,
        organization_ids: list[str],
        timeout: str | int | None = None,
    ) -> PaymentTypesResponse:
        """Payment types.

        Args:
            organization_ids (list[str]): Organizations IDs which payment types have to be returned.
                Can be obtained by `/api/1/organizations` operation.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1payment_types/post
        """
        response = await self._client.request(
            "/api/1/payment_types",
            data={
                "organizationIds": organization_ids,
            },
            timeout=timeout,
        )
        return PaymentTypesResponse(**orjson.loads(response.content))

    async def removal_types(
        self,
        organization_ids: list[str],
        timeout: str | int | None = None,
    ) -> RemovalTypesResponse:
        """Removal types (reasons for deletion).

        Args:
            organization_ids (list[str]): Organizations IDs which payment types have to be returned.
                Can be obtained by `/api/1/organizations` operation.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1removal_types/post
        """
        response = await self._client.request(
            "/api/1/removal_types",
            data={
                "organizationIds": organization_ids,
            },
            timeout=timeout,
        )
        return RemovalTypesResponse(**orjson.loads(response.content))

    async def tips_types(
        self,
        timeout: str | int | None = None,
    ) -> TipsTypesResponse:
        """Get tips types for api-login`s rms group.

        Args:
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1tips_types/post
        """
        response = await self._client.request(
            "/api/1/tips_types",
            timeout=timeout,
        )
        return TipsTypesResponse(**orjson.loads(response.content))

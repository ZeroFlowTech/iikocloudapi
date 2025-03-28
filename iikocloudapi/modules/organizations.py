import enum
from decimal import Decimal
from typing import Literal

import orjson
from pydantic import BaseModel, Field

from iikocloudapi.client import Client
from iikocloudapi.helpers import BaseResponseModel, ExternalData, partial_model

Parameters = Literal[
    "PricesVatInclusive",
    "LoyaltyDiscountAffectsVat",
    "Version",
    "AddressFormatType",
    "IsAnonymousGuestsAllowed",
    "Name",
    "Country",
    "RestaurantAddress",
    "Latitude",
    "Longitude",
    "UseUaeAddressingSystem",
    "CountryPhoneCode",
    "MarketingSourceRequiredInDelivery",
    "DefaultDeliveryCityId",
    "DeliveryCityIds",
    "DeliveryServiceType",
    "DefaultCallCenterPaymentTypeId",
    "OrderItemCommentEnabled",
    "IsConfirmationEnabled",
    "ConfirmAllowedIntervalInMinutes",
    "AddressLookup",
    "UseBusinessHoursAndMapping",
    "DeliveryOrderPaymentSettings",
    "CurrencyIsoName",
]


class OrganizationSimpleModel(BaseModel):
    class ResponseTypeEnum(str, enum.Enum):
        simple = "Simple"
        extended = "Extended"

    id: str
    name: str
    code: str | None = None
    external_data: list[ExternalData] | None = Field(None, alias="externalData")
    response_type: ResponseTypeEnum = Field(alias="responseType")


class OrganizationExtendedModel(OrganizationSimpleModel):
    class DeliveryServiceTypeEnum(str, enum.Enum):
        courier_only = "CourierOnly"
        self_service_only = "SelfServiceOnly"
        courier_and_self_service = "CourierAndSelfService"

    class DeliveryOrderPaymentSettingsEnum(str, enum.Enum):
        when_order_on_the_way = "WhenOrderOnTheWay"
        when_order_closed = "WhenOrderClosed"

    class AddressFormatTypeEnum(str, enum.Enum):
        legacy = "Legacy"
        city = "City"
        international = "International"
        int_no_postcode = "IntNoPostcode"

    class AddressLookupEnum(str, enum.Enum):
        dadata = "DaData"
        getaddress = "GetAddress"
        ya = "Ya"

    country: str | None = None
    restaurant_address: str | None = Field(None, alias="restaurantAddress")
    latitude: Decimal
    longitude: Decimal
    use_uae_addressing_system: bool = Field(alias="useUaeAddressingSystem")
    version: str
    currency_iso_name: str | None = Field(None, alias="currencyIsoName")
    currency_minimum_denomination: Decimal | None = Field(None, alias="currencyMinimumDenomination")
    country_phone_code: str | None = Field(None, alias="countryPhoneCode")
    marketing_source_required_in_delivery: bool | None = Field(None, alias="marketingSourceRequiredInDelivery")
    default_delivery_city_id: str | None = Field(None, alias="defaultDeliveryCityId")
    delivery_city_ids: list[str] | None = Field(None, alias="deliveryCityIds")
    delivery_service_type: DeliveryServiceTypeEnum | None = Field(None, alias="deliveryServiceType")
    delivery_order_payment_settings: DeliveryOrderPaymentSettingsEnum | None = Field(
        None, alias="deliveryOrderPaymentSettings"
    )
    default_call_center_payment_type_id: str | None = Field(None, alias="defaultCallCenterPaymentTypeId")
    order_item_comment_enabled: bool | None = Field(None, alias="orderItemCommentEnabled")
    inn: str | None = None
    address_format_type: AddressFormatTypeEnum = Field(alias="addressFormatType")
    is_confirmation_enabled: bool | None = Field(None, alias="isConfirmationEnabled")
    confirm_allowed_interval_in_minutes: int | None = Field(None, alias="confirmAllowedIntervalInMinutes")
    is_cloud: bool = Field(alias="isCloud")
    is_anonymous_guests_allowed: bool = Field(alias="isAnonymousGuestsAllowed")
    address_lookup: list[AddressLookupEnum] = Field(alias="addressLookup")


@partial_model
class OrganizationExtendedOptionalModel(OrganizationExtendedModel):
    pass


class OrganizationsResponse(BaseResponseModel):
    organizations: list[OrganizationSimpleModel | OrganizationExtendedModel]

    @property
    def organization_ids(self) -> list:
        return [org.id for org in self.organizations]


class OrganizationsSettingsResponse(BaseResponseModel):
    organizations: list[OrganizationExtendedOptionalModel]


class Organizations:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def __call__(
        self,
        organization_ids: list[str] | None = None,
        return_additional_info: bool = False,
        include_disabled: bool = False,
        return_external_data: list[str] | None = None,
        timeout: str | int | None = None,
    ) -> OrganizationsResponse:
        """Returns organizations available to api-login user.

        Args:
            organization_ids (list[str] | None, optional): Organizations IDs which have to be returned.
                By default - all organizations from apiLogin. Can be obtained by `/api/1/organizations` operation.
                Defaults to None.
            return_additional_info (bool, optional): A sign whether additional information about the organization
                should be returned (RMS version, country, restaurantAddress, etc.), or only minimal information
                should be returned (id and name).
                Defaults to False.
            include_disabled (bool, optional): Attribute that shows that response contains disabled organizations.
                Defaults to False.
            return_external_data (list[str] | None, optional): External data keys that have to be returned.
                Defaults to None.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Organizations/paths/~1api~11~1organizations/post
        """
        response = await self._client.request(
            "/api/1/organizations",
            data={
                "organizationIds": organization_ids,
                "returnAdditionalInfo": return_additional_info,
                "includeDisabled": include_disabled,
                "returnExternalData": return_external_data,
            },
            timeout=timeout,
        )
        return OrganizationsResponse(**orjson.loads(response.content))

    async def settings(
        self,
        parameters: list[Parameters],
        organization_ids: list[str] | None = None,
        include_disabled: bool = False,
        return_external_data: list[str] | None = None,
        timeout: str | int | None = None,
    ) -> OrganizationsSettingsResponse:
        """Returns available to api-login user organizations specified settings.

        Args:
            organization_ids (list[str] | None, optional): Organizations IDs which have to be returned.
                By default - all organizations from apiLogin. Defaults to None.
            include_disabled (bool, optional): Attribute that shows that response contains disabled organizations.
                Defaults to False.
            parameters (list[Parameters] | None, optional): Parameters of information to be present in response.
                Defaults to None.
            return_external_data (list[str] | None, optional): External data keys that have to be returned.
                Defaults to None.
            timeout (str | int | None, optional): Timeout in seconds.
                Defaults to None.

        Ref: https://api-ru.iiko.services/#tag/Organizations/paths/~1api~11~1organizations~1settings/post
        """
        response = await self._client.request(
            "/api/1/organizations/settings",
            data={
                "organizationIds": organization_ids,
                "includeDisabled": include_disabled,
                "parameters": parameters or [],
                "returnExternalData": return_external_data,
            },
            timeout=timeout,
        )
        return OrganizationsSettingsResponse(**orjson.loads(response.content))

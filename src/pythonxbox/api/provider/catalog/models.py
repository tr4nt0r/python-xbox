from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import Field, field_validator

from pythonxbox.common.models import PascalCaseModel


class AlternateIdType(StrEnum):
    LEGACY_XBOX_PRODUCT_ID = "LegacyXboxProductId"
    XBOX_TITLE_ID = "XboxTitleId"
    PACKAGE_FAMILY_NAME = "PackageFamilyName"


class FieldsTemplate(StrEnum):
    BROWSE = "browse"
    DETAILS = "details"


class PlatformType(StrEnum):
    XBOX = "windows.xbox"
    DESKTOP = "windows.desktop"


class Image(PascalCaseModel):
    file_id: str | None = None
    eis_listing_identifier: Any = Field(None, alias="EISListingIdentifier")
    background_color: str | None = None
    caption: str | None = None
    file_size_in_bytes: int
    foreground_color: str | None = None
    height: int
    image_position_info: str | None = None
    image_purpose: str
    unscaled_image_sha256_hash: str | None = Field(
        None, alias="UnscaledImageSHA256Hash"
    )
    uri: str
    width: int


class Video(PascalCaseModel):
    uri: str
    video_purpose: str
    height: int
    width: int
    audio_encoding: str
    video_encoding: str
    video_position_info: str
    caption: str
    file_size_in_bytes: int
    preview_image: Image
    sort_order: int


class SearchTitle(PascalCaseModel):
    search_title_string: str
    search_title_type: str


class ContentRating(PascalCaseModel):
    rating_system: str
    rating_id: str
    rating_descriptors: list[str]
    rating_disclaimers: list
    interactive_elements: list | None = None


class UsageData(PascalCaseModel):
    aggregate_time_span: str
    average_rating: float
    play_count: int | None = None
    rating_count: int
    rental_count: str | None = None
    trial_count: str | None = None
    purchase_count: str | None = None


class ProductProperties(PascalCaseModel):
    attributes: list | None = None
    can_install_to_sd_card: bool | None = Field(None, alias="CanInstallToSDCard")
    category: str | None = None
    sub_category: str | None = None
    categories: list[str] | None = None
    extensions: Any = None
    is_accessible: bool | None = None
    is_line_of_business_app: bool | None = None
    is_published_to_legacy_windows_phone_store: bool | None = None
    is_published_to_legacy_windows_store: bool | None = None
    is_settings_app: bool | None = None
    package_family_name: str | None = None
    package_identity_name: str | None = None
    publisher_certificate_name: str | None = None
    publisher_id: str
    xbox_live_tier: Any = None
    xbox_xpa: Any = Field(None, alias="XboxXPA")
    xbox_cross_gen_set_id: Any = None
    xbox_console_gen_optimized: Any = None
    xbox_console_gen_compatible: Any = None
    xbox_live_gold_required: bool | None = None
    ownership_type: Any = None
    pdp_background_color: str | None = None
    has_add_ons: bool | None = None
    revision_id: str
    product_group_id: str | None = None
    product_group_name: str | None = None


class AlternateId(PascalCaseModel):
    id_type: str
    value: str


class ValidationData(PascalCaseModel):
    passed_validation: bool
    revision_id: str
    validation_result_uri: str | None = None


class FulfillmentData(PascalCaseModel):
    product_id: str
    wu_bundle_id: str | None = None
    wu_category_id: str
    package_family_name: str
    sku_id: str
    content: Any = None
    package_features: Any = None


class HardwareProperties(PascalCaseModel):
    minimum_hardware: list
    recommended_hardware: list
    minimum_processor: Any = None
    recommended_processor: Any = None
    minimum_graphics: Any = None
    recommended_graphics: Any = None


class Application(PascalCaseModel):
    application_id: str
    declaration_order: int
    extensions: list[str]


class FrameworkDependency(PascalCaseModel):
    max_tested: int
    min_version: int
    package_identity: str


class PlatformDependency(PascalCaseModel):
    max_tested: int | None = None
    min_version: int | None = None
    platform_name: str


class Package(PascalCaseModel):
    applications: list[Application] | None = None
    architectures: list[str]
    capabilities: list[str] | None = None
    device_capabilities: list[str] | None = None
    experience_ids: list | None = None
    framework_dependencies: list[FrameworkDependency] | None = None
    hardware_dependencies: list | None = None
    hardware_requirements: list | None = None
    hash: str | None = None
    hash_algorithm: str | None = None
    is_streaming_app: bool | None = None
    languages: list[str] | None = None
    max_download_size_in_bytes: int
    max_install_size_in_bytes: int | None = None
    package_format: str
    package_family_name: str | None = None
    main_package_family_name_for_dlc: Any = None
    package_full_name: str | None = None
    package_id: str
    content_id: str
    key_id: str | None = None
    package_rank: int | None = None
    package_uri: str | None = None
    platform_dependencies: list[PlatformDependency] | None = None
    platform_dependency_xml_blob: str | None = None
    resource_id: str | None = None
    version: str | None = None
    package_download_uris: Any = None
    driver_dependencies: list | None = None
    fulfillment_data: FulfillmentData | None = None


class LegalText(PascalCaseModel):
    additional_license_terms: str
    copyright: str
    copyright_uri: str
    privacy_policy: str
    privacy_policy_uri: str
    tou: str
    tou_uri: str


class SkuLocalizedProperty(PascalCaseModel):
    contributors: list | None = None
    features: list | None = None
    minimum_notes: str | None = None
    recommended_notes: str | None = None
    release_notes: str | None = None
    display_platform_properties: Any = None
    sku_description: str
    sku_title: str
    sku_button_title: str | None = None
    delivery_date_overlay: Any = None
    sku_display_rank: list | None = None
    text_resources: Any = None
    images: list | None = None
    legal_text: LegalText | None = None
    language: str
    markets: list[str]


class SkuMarketProperty(PascalCaseModel):
    first_available_date: datetime | str | None = None
    supported_languages: list[str] | None = None
    package_ids: Any = None
    pi_filter: Any = Field(None, alias="PIFilter")
    markets: list[str]


class SkuProperties(PascalCaseModel):
    early_adopter_enrollment_url: Any = None
    fulfillment_data: FulfillmentData | None = None
    fulfillment_type: str | None = None
    fulfillment_plugin_id: Any = None
    has_third_party_iaps: bool | None = Field(None, alias="HasThirdPartyIAPs")
    last_update_date: datetime | None = None
    hardware_properties: HardwareProperties | None = None
    hardware_requirements: list | None = None
    hardware_warning_list: list | None = None
    installation_terms: str
    packages: list[Package] | None = None
    version_string: str | None = None
    visible_to_b2b_service_ids: list = Field(alias="VisibleToB2BServiceIds")
    xbox_xpa: bool | None = Field(None, alias="XboxXPA")
    bundled_skus: list | None = None
    is_repurchasable: bool
    sku_display_rank: int
    display_physical_store_inventory: Any = None
    additional_identifiers: list
    is_trial: bool
    is_pre_order: bool
    is_bundle: bool

    @field_validator("last_update_date", mode="before", check_fields=True)
    def validator(x: "SkuProperties") -> "SkuProperties":
        return x or None


class Sku(PascalCaseModel):
    last_modified_date: datetime
    localized_properties: list[SkuLocalizedProperty]
    market_properties: list[SkuMarketProperty]
    product_id: str
    properties: SkuProperties
    sku_a_schema: str
    sku_b_schema: str
    sku_id: str
    sku_type: str
    recurrence_policy: Any = None
    subscription_policy_id: Any = None


class AllowedPlatform(PascalCaseModel):
    max_version: int | None = None
    min_version: int | None = None
    platform_name: str


class ClientConditions(PascalCaseModel):
    allowed_platforms: list[AllowedPlatform]


class Conditions(PascalCaseModel):
    client_conditions: ClientConditions
    end_date: datetime
    resource_set_ids: list[str]
    start_date: datetime


class PIFilter(PascalCaseModel):
    exclusion_properties: list
    inclusion_properties: list


class Price(PascalCaseModel):
    currency_code: str
    is_pi_required: bool = Field(alias="IsPIRequired")
    list_price: float
    msrp: float = Field(alias="MSRP")
    tax_type: str
    wholesale_currency_code: str


class OrderManagementData(PascalCaseModel):
    granted_entitlement_keys: list | None = None
    pi_filter: PIFilter | None = Field(None, alias="PIFilter")
    price: Price


class AvailabilityProperties(PascalCaseModel):
    original_release_date: datetime | None = None


class SatisfyingEntitlementKey(PascalCaseModel):
    entitlement_keys: list[str]
    licensing_key_ids: list[str]


class LicensingData(PascalCaseModel):
    satisfying_entitlement_keys: list[SatisfyingEntitlementKey]


class Availability(PascalCaseModel):
    actions: list[str]
    availability_a_schema: str | None = None
    availability_b_schema: str | None = None
    availability_id: str | None = None
    conditions: Conditions | None = None
    last_modified_date: datetime | None = None
    markets: list[str] | None = None
    order_management_data: OrderManagementData | None = None
    properties: AvailabilityProperties | None = None
    sku_id: str | None = None
    display_rank: int | None = None
    remediation_required: bool | None = None
    licensing_data: LicensingData | None = None


class DisplaySkuAvailability(PascalCaseModel):
    sku: Sku | None = None
    availabilities: list[Availability]


class LocalizedProperty(PascalCaseModel):
    developer_name: str | None = None
    display_platform_properties: Any | None = None
    publisher_name: str | None = None
    publisher_website_uri: str | None = None
    support_uri: str | None = None
    eligibility_properties: Any | None = None
    franchises: list | None = None
    images: list[Image]
    videos: list[Video] | None = None
    product_description: str | None = None
    product_title: str
    short_title: str | None = None
    sort_title: str | None = None
    friendly_title: str | None = None
    short_description: str | None = None
    search_titles: list[SearchTitle] | None = None
    voice_title: str | None = None
    render_group_details: Any | None = None
    product_display_ranks: list | None = None
    interactive_model_config: Any | None = None
    interactive_3d_enabled: bool | None = Field(None, alias="Interactive3DEnabled")
    language: str | None = None
    markets: list[str] | None = None


class MarketProperty(PascalCaseModel):
    original_release_date: datetime | None = None
    original_release_friendly_name: str | None = None
    minimum_user_age: int | None = None
    content_ratings: list[ContentRating] | None = None
    related_products: list | None = None
    usage_data: list[UsageData]
    bundle_config: Any | None = None
    markets: list[str] | None = None


class Product(PascalCaseModel):
    last_modified_date: datetime | None = None
    localized_properties: list[LocalizedProperty]
    market_properties: list[MarketProperty]
    product_a_schema: str | None = None
    product_b_schema: str | None = None
    product_id: str
    properties: ProductProperties | None = None
    alternate_ids: list[AlternateId] | None = None
    domain_data_version: Any | None = None
    ingestion_source: str | None = None
    is_microsoft_product: bool | None = None
    preferred_sku_id: str | None = None
    product_type: str | None = None
    validation_data: ValidationData | None = None
    merchandizing_tags: list | None = None
    part_d: str | None = None
    product_family: str
    schema_version: str | None = None
    product_kind: str
    display_sku_availabilities: list[DisplaySkuAvailability]


class CatalogResponse(PascalCaseModel):
    big_ids: list[str] | None = None
    has_more_pages: bool | None = None
    products: list[Product]
    total_result_count: int | None = None


class SearchProduct(PascalCaseModel):
    background_color: str | None = None
    height: int | None = None
    image_type: str | None = None
    width: int | None = None
    platform_properties: list
    icon: str | None = None
    product_id: str
    type: str
    title: str


class CatalogSearchResult(PascalCaseModel):
    product_family_name: str
    products: list[SearchProduct]


class CatalogSearchResponse(PascalCaseModel):
    results: list[CatalogSearchResult]
    total_result_count: int

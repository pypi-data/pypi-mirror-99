import enum

_EVE_IMAGE_SERVER_URL = "https://images.evetech.net"
_DEFAULT_IMAGE_SIZE = 32


class EsiCategory(enum.Enum):
    """Enum class for ESI categories"""

    ALLIANCE = enum.auto()
    CHARACTER = enum.auto()
    CORPORATION = enum.auto()
    FACTION = enum.auto()
    TYPE = enum.auto()


class ImageVariant(enum.Enum):
    """Enum class for image variants"""

    LOGO = "logo"
    PORTRAIT = "portrait"
    ICON = "icon"
    RENDER = "render"
    BPO = "bp"
    BPC = "bpc"


class EsiTenant(enum.Enum):
    """Enum class for ESI tenants"""

    TRANQUILITY = "tranquility"


def _eve_entity_image_url(
    category: str,
    entity_id: int,
    size: int = 32,
    variant: ImageVariant = None,
    tenant: EsiTenant = None,
) -> str:
    """returns image URL for an Eve Online ID.
    Supported categories: alliance, corporation, character, inventory_type

    Arguments:
    - category: category of the ID, see ESI category constants
    - entity_id: Eve ID of the entity
    - size: (optional) render size of the image.must be between 32 (default) and 1024
    - variant: (optional) image variant for category.
    - tenant: (optional) Eve Server, either `tranquility`(default) or `singularity`

    Returns:
    - URL string for the requested image on the Eve image server

    Exceptions:
    - Throws ValueError on invalid input
    """

    # input validations
    categories = {
        EsiCategory.ALLIANCE: {
            "endpoint": "alliances",
            "variants": [ImageVariant.LOGO],
        },
        EsiCategory.CORPORATION: {
            "endpoint": "corporations",
            "variants": [ImageVariant.LOGO],
        },
        EsiCategory.CHARACTER: {
            "endpoint": "characters",
            "variants": [ImageVariant.PORTRAIT],
        },
        EsiCategory.FACTION: {
            "endpoint": "corporations",
            "variants": [ImageVariant.LOGO],
        },
        EsiCategory.TYPE: {
            "endpoint": "types",
            "variants": [
                ImageVariant.ICON,
                ImageVariant.RENDER,
                ImageVariant.BPO,
                ImageVariant.BPC,
            ],
        },
    }
    if not entity_id:
        raise ValueError("Invalid entity_id: {}".format(entity_id))
    else:
        entity_id = int(entity_id)

    if not size or size < 32 or size > 1024 or (size & (size - 1) != 0):
        raise ValueError("Invalid size: {}".format(size))

    if type(category) is not EsiCategory:
        raise ValueError("Invalid category {}".format(category))
    else:
        endpoint = categories[category]["endpoint"]

    if variant:
        if variant not in categories[category]["variants"]:
            raise ValueError(
                "Invalid variant {} for category {}".format(variant, category)
            )
    else:
        variant = categories[category]["variants"][0]

    if tenant and type(tenant) is not EsiTenant:
        raise ValueError("Invalid tenant {}".format(tenant))

    # compose result URL
    result = "{}/{}/{}/{}?size={}".format(
        _EVE_IMAGE_SERVER_URL, endpoint, entity_id, variant.value, size
    )
    if tenant:
        result += "&tenant={}".format(tenant.value)

    return result


def alliance_logo_url(alliance_id: int, size: int = _DEFAULT_IMAGE_SIZE) -> str:
    """image URL for the given alliance ID"""
    return _eve_entity_image_url(EsiCategory.ALLIANCE, alliance_id, size)


def corporation_logo_url(corporation_id: int, size: int = _DEFAULT_IMAGE_SIZE) -> str:
    """image URL for the given corporation ID"""
    return _eve_entity_image_url(EsiCategory.CORPORATION, corporation_id, size)


def character_portrait_url(character_id: int, size: int = _DEFAULT_IMAGE_SIZE) -> str:
    """image URL for the given character ID"""
    return _eve_entity_image_url(EsiCategory.CHARACTER, character_id, size)


def faction_logo_url(faction_id: int, size: int = _DEFAULT_IMAGE_SIZE) -> str:
    """image URL for the given alliance ID"""
    return _eve_entity_image_url(EsiCategory.FACTION, faction_id, size)


def type_icon_url(type_id: int, size: int = _DEFAULT_IMAGE_SIZE) -> str:
    """icon image URL for the given type ID"""
    return _eve_entity_image_url(
        EsiCategory.TYPE, type_id, size, variant=ImageVariant.ICON
    )


def type_render_url(type_id: int, size: int = _DEFAULT_IMAGE_SIZE) -> str:
    """render image URL for the given type ID"""
    return _eve_entity_image_url(
        EsiCategory.TYPE, type_id, size, variant=ImageVariant.RENDER
    )


def type_bp_url(type_id: int, size: int = _DEFAULT_IMAGE_SIZE) -> str:
    """blueprint original image URL for the given type ID"""
    return _eve_entity_image_url(
        EsiCategory.TYPE, type_id, size, variant=ImageVariant.BPO
    )


def type_bpc_url(type_id: int, size: int = _DEFAULT_IMAGE_SIZE) -> str:
    """blueprint copy image URL for the given type ID"""
    return _eve_entity_image_url(
        EsiCategory.TYPE, type_id, size, variant=ImageVariant.BPC
    )

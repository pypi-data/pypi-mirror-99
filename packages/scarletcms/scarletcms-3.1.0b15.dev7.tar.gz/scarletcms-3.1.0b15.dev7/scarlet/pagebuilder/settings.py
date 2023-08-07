from django.conf import settings

SITE_NAME = getattr(settings, "SITE_NAME", "Wonderful")

DEFAULT_WIDE_SIZES = {
    "wide_desktop": {
        "width": 1920,
        "height": 1080,
        "editable": True,
        "upscale": False,
    },
    "wide_mobile": {"width": 580, "height": 720, "editable": True, "upscale": False,},
}

WIDE_IMAGE_SIZES = getattr(settings, "WIDE_IMAGE_SIZES", DEFAULT_WIDE_SIZES)

DEFAULT_SQUARE_SIZES = {
    "square_desktop": {"width": 960, "height": 720, "upscale": False,},
    "square_mobile": {"width": 580, "height": 386, "upscale": False,},
}

SQUARE_IMAGE_SIZES = getattr(settings, "SQUARE_IMAGE_SIZES", DEFAULT_SQUARE_SIZES)


DEFAULT_CAROUSEL_IMAGE_SIZES = {
    "carousel_desktop": {"width": 960, "height": 720, "upscale": False,},
    "carousel_mobile": {"width": 580, "height": 386, "upscale": False,},
}

CAROUSEL_IMAGE_SIZES = getattr(
    settings, "CAROUSEL_IMAGE_SIZES", DEFAULT_CAROUSEL_IMAGE_SIZES
)

DEFAULT_GALLERY_IMAGE_SIZES = {
    "gallery_desktop": {"width": 960, "height": 720, "upscale": False,},
    "gallery_mobile": {"width": 580, "height": 386, "upscale": False,},
}

GALLERY_IMAGE_SIZES = getattr(
    settings, "GALLERY_IMAGE_SIZES", DEFAULT_GALLERY_IMAGE_SIZES
)

# Pagebuilder Models
HERO_MODULE = "hero"
HEADER_MODULE = "header"
FAQ_MODULE = "faq"
TWO_COLUMN_MODULE = "two-column"
ICON_LIST_MODULE = "icon-list"
LOCATION_MODULE = "locations"
GALLERY_MODULE = "gallery"
CAROUSEL_MODULE = "carousel"
ICON_LIST_ITEM = "icon"
FAQ_ITEM = "faq-item"
LOCATION_ITEM = "location-item"
GALLERY_ITEM = "image"
CAROUSEL_ITEM = "slide"

MODULE_TYPES = (
    HERO_MODULE,
    HEADER_MODULE,
    FAQ_MODULE,
    TWO_COLUMN_MODULE,
    LOCATION_MODULE,
    ICON_LIST_MODULE,
    GALLERY_MODULE,
    CAROUSEL_MODULE,
)

# If you copy default_models into your project using an app named Pages,
# all these settings can remain unchanged.
PAGE_MODEL = getattr(settings, "PAGE_MODEL", "pages.Page")

HERO_MODULE_MODEL = getattr(settings, "HERO_MODULE_MODEL", "pages.HeroModule")
HEADER_MODULE_MODEL = getattr(settings, "HEADER_MODULE_MODEL", "pages.HeaderModule")
TWO_COLUMN_MODEL = getattr(settings, "TWO_COLUMN_MODEL", "pages.TwoColumnModule")
ICON_LIST_MODEL = getattr(settings, "ICON_LIST_MODEL", "pages.IconListModule")
FAQ_MODULE_MODEL = getattr(settings, "FAQ_MODULE_MODEL", "pages.FAQModule")
LOCATION_MODULE_MODEL = getattr(
    settings, "LOCATION_MODULE_MODEL", "pages.LocationModule"
)
GALLERY_MODULE_MODEL = getattr(
    settings, "GALLERY_MODULE_MODEL", "pages.ImageGalleryModule"
)
CAROUSEL_MODULE_MODEL = getattr(
    settings, "CAROUSEL_MODULE_MODEL", "pages.CarouselModule"
)

ICON_LIST_ITEM_MODEL = getattr(settings, "ICON_LIST_ITEM_MODEL", "pages.IconListItem")
FAQ_ITEM_MODEL = getattr(settings, "FAQ_ITEM_MODEL", "pages.FAQItem")
LOCATION_ITEM_MODEL = getattr(settings, "LOCATION_ITEM_MODEL", "pages.LocationItem")
GALLERY_ITEM_MODEL = getattr(settings, "GALLERY_ITEM_MODEL", "pages.GalleryImage")
CAROUSEL_ITEM_MODEL = getattr(settings, "CAROUSEL_ITEM_MODEL", "pages.CarouselItem")

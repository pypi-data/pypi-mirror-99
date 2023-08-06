"""Store various application values."""


class AppKeys:
    """Store application keys in one place."""

    GITHUB_TOKEN = 'GITHUB_TOKEN'
    VAULT_ADDR = 'VAULT_ADDR'

    IMAGE_API_RELATIVE_URL = 'image_api_relative_url'
    IMAGE_ENHANCE_API_RELATIVE_URL = 'image_enhance_api_relative_url'


class ImageVariants:
    """Allowed values for the image variant parameter."""

    STANDARD = 'standard'
    THUMBNAIL = 'thumbnail'
    ORIGINAL = 'original'
    DEFAULT = STANDARD

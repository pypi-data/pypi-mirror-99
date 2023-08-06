"""Store various application values."""
from typing import List


class AppKeys:
    """Store application keys in one place."""

    GITHUB_TOKEN = 'GITHUB_TOKEN'
    VAULT_ADDR = 'VAULT_ADDR'

    IMAGE_API_RELATIVE_URL = 'image_api_relative_url'
    IMAGE_ENHANCE_API_RELATIVE_URL = 'image_enhance_api_relative_url'


class LouvreSecretPathNames:
    """Store the secret path names that need to be set as environment variables 
    in order to use this package."""

    ISSUER = 'ISSUER'

    TOKEN_ENDPOINT = 'TOKEN_ENDPOINT'
    CLIENT_ID_API = 'CLIENT_ID_API'
    CLIENT_SECRET_API = 'CLIENT_SECRET_API'
    LOUVRE_DOMAIN = 'LOUVRE_DOMAIN'

    # Training against PROD
    TOKEN_ENDPOINT_PROD = 'TOKEN_ENDPOINT_PROD'
    CLIENT_ID_API_PROD = 'CLIENT_ID_API_PROD'
    CLIENT_SECRET_API_PROD = 'CLIENT_SECRET_API_PROD'
    LOUVRE_DOMAIN_PROD = 'LOUVRE_DOMAIN_PROD'

    @classmethod
    def get_all(cls) -> List[str]:
        """
        Return all the class members.
        """
        return [
            attr for attr in dir(cls)
            if not callable(getattr(cls, attr)) and not attr.startswith("__")
        ]


class ImageVariants:
    """Allowed values for the image variant parameter."""

    STANDARD = 'standard'
    THUMBNAIL = 'thumbnail'
    ORIGINAL = 'original'
    DEFAULT = STANDARD

"""This class is in its own module to avoid import issues."""

import os
from .enums import LouvreSecretPathNames


class SecretPaths:
    """Store secret paths used against the vault service."""

    TOKEN_ENDPOINT = os.environ[LouvreSecretPathNames.TOKEN_ENDPOINT]
    CLIENT_ID_API = os.environ[LouvreSecretPathNames.CLIENT_ID_API]
    CLIENT_SECRET_API = os.environ[LouvreSecretPathNames.CLIENT_SECRET_API]
    LOUVRE_DOMAIN = os.environ[LouvreSecretPathNames.LOUVRE_DOMAIN]

    # Against PROD
    TOKEN_ENDPOINT_PROD = os.environ[LouvreSecretPathNames.TOKEN_ENDPOINT_PROD]
    CLIENT_ID_API_PROD = os.environ[LouvreSecretPathNames.CLIENT_ID_API_PROD]
    CLIENT_SECRET_API_PROD = os.environ[
        LouvreSecretPathNames.CLIENT_SECRET_API_PROD]
    LOUVRE_DOMAIN_PROD = os.environ[LouvreSecretPathNames.LOUVRE_DOMAIN_PROD]

    ISSUER = os.environ[LouvreSecretPathNames.ISSUER]

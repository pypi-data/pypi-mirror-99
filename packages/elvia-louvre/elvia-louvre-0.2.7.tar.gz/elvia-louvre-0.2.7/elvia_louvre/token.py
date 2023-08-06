"""
Module with methods to authenticate against ImageAPI and ImageEnhanceAPI.
"""

from datetime import datetime, timedelta
from typing import Dict
from elvia_vault.vault_client import VaultClient
import requests
from .config import Config
from .secret_paths import SecretPaths


class Token():
    """Class for working with jwt tokens."""

    _tokens: Dict[str, str] = {}
    _expiry: Dict[str, datetime] = {}

    @classmethod
    def get_token(cls, using_production_images: bool = False) -> str:
        """Return the current token if still valid, else a new one.
           Assume that the token life has ended when time is not smaller than:
           _expiry minus the buffer"""

        endpoint: str = cls._get_token_endpoint(using_production_images)
        if endpoint in cls._tokens.keys() and endpoint in cls._expiry.keys(
        ) and datetime.now() < cls._expiry[endpoint] - timedelta(
                seconds=Config.token_buffer_seconds):
            return cls._tokens[endpoint]
        return cls.get_new_token(
            using_production_images=using_production_images)

    @classmethod
    def get_new_token(cls, using_production_images: bool = False) -> str:
        """Create and get token for this API to communicate with ImageAPI and ImageEnhanceAPI.
           Assume the expiry time is found by adding expires_in to the time right before triggering the request."""
        tick = datetime.now()
        endpoint: str = cls._get_token_endpoint(using_production_images)

        token_response = requests.post(
            url=Config.get_secret(endpoint),
            headers={},
            data={
                'grant_type':
                'client_credentials',
                'client_id':
                Config.get_secret(
                    cls._get_client_id_api(using_production_images)),
                'client_secret':
                Config.get_secret(
                    cls._get_client_secret_api(using_production_images))
            })

        cls._tokens[endpoint] = token_response.json()['access_token']
        cls._expiry[endpoint] = tick + timedelta(
            seconds=int(token_response.json()['expires_in']))
        return cls._tokens[endpoint]

    @classmethod
    def get_headers(cls, using_production_images: bool = False) -> dict:
        """Return headers to be used in HTTP requests against ImageAPI / ImageEnhanceAPI."""
        return {
            "Authorization":
            "Bearer {}".format(
                cls.get_token(
                    using_production_images=using_production_images)),
            'Content-Type':
            'application/json'
        }

    @staticmethod
    def _get_token_endpoint(using_production_images: bool) -> str:
        if using_production_images:
            return SecretPaths.TOKEN_ENDPOINT_PROD
        if not VaultClient.is_in_cluster():
            return SecretPaths.TOKEN_ENDPOINT_TEST
        return SecretPaths.TOKEN_ENDPOINT

    @staticmethod
    def _get_client_id_api(using_production_images: bool) -> str:
        if using_production_images:
            return SecretPaths.CLIENT_ID_API_PROD
        if not VaultClient.is_in_cluster():
            return SecretPaths.CLIENT_ID_API_TEST
        return SecretPaths.CLIENT_ID_API

    @staticmethod
    def _get_client_secret_api(using_production_images: bool) -> str:
        if using_production_images:
            return SecretPaths.CLIENT_SECRET_API_PROD
        if not VaultClient.is_in_cluster():
            return SecretPaths.CLIENT_SECRET_API_TEST
        return SecretPaths.CLIENT_SECRET_API

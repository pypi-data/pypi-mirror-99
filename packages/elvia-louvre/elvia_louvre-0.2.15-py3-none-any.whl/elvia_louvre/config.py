from typing import Union

from elvia_vault import VaultClient
from .errors import LouvreVaultConnError, LouvreSecretError
from .data_models import SecretPathSets


class Config():
    """Configuration values and secrets."""

    vault: VaultClient
    secrets: dict = {}
    _secret_path_sets: SecretPathSets

    # ImageAPI - GraphQL API to fetch images
    image_api_relative_url: str = '/image/graphql'

    # ImageEnhanceAPI - API to update image's metadata
    image_enhance_api_relative_url: str = '/imageenhance/Metadata'

    # Token buffer in seconds
    token_buffer_seconds: int = 60

    def __init__(self,
                 secret_path_sets: SecretPathSets,
                 github_token: Union[str, None] = None):
        """        
        Connects to the vault using VAULT_ADDR from os.environ.
        If cluster, it uses kubernetes auth, else the Github token.

        Raises
        ------
        LouvreVaultConnError
        """
        # Clean up, to avoid mixing secrets from different vaults, in the case
        # VAULT_ADDR changes between calls
        self.secrets = {}
        self._secret_path_sets = secret_path_sets
        # Get a fresh VaultClient instance and connect to the vault service
        try:
            self.vault = VaultClient(github_token=github_token)
        except Exception as exception:
            raise LouvreVaultConnError(str(exception))

    def get_secret(self, secret_path: str) -> str:
        """
        Return a secret value given a secret path.
        Fetch from vault only if not previously fetched.

        Parameters
        ----------
        secret_path : str

        Raises
        ------
        LouvreSecretError
        """
        try:
            if not secret_path in self.secrets.keys():
                self.secrets[secret_path] = self.vault.get_value(secret_path)
            return self.secrets[secret_path]

        except KeyError as exception:
            raise LouvreSecretError(exception)

    def secret_path_sets(self) -> SecretPathSets:
        if '_secret_path_sets' in vars(self):
            return self._secret_path_sets
        raise LouvreSecretError()

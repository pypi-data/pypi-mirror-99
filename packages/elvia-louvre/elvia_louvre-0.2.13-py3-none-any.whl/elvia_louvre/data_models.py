from dataclasses import dataclass, field
from elvia_louvre.errors import LouvreSecretError
from typing import Dict, List, Optional, Union


@dataclass
class ImageFile:
    """Represent image files from ImageAPI."""

    image_variant: str
    size: int
    sasuri: str
    height: float
    width: float


@dataclass
class ImageData:
    """Represent image data from ImageAPI."""

    image_id: str
    etag: str
    metadata: List[dict]
    image_files: List[ImageFile]

    @property
    def image_variants(self) -> List[str]:
        """
        Return a list with the imageVariants present.
        """
        return [image_file.image_variant for image_file in self.image_files]

    def get_variant(self, variant: str) -> Union[ImageFile, None]:
        """
        Given an image variant, return its corresponding ImageFile if it exits in the ImageData 
        instance.

        Parameters
        ----------
        variant : str
            Name of the desired image variant.

        Returns
        -------
        ImageFile, None
        """
        for image_file in self.image_files:
            if variant == image_file.image_variant:
                return image_file
        return None


@dataclass
class UpdateMetadataRequest:
    """Represent a metadata update request to be sent to ImageEnhanceAPI."""

    image_id: str
    additional_metadata: Dict[str, str] = field(default_factory=dict)
    plugin_id: Optional[str] = None
    e_tag: Optional[str] = None
    skip_e_tag_validation: bool = True
    client_name: str = 'python-client'


@dataclass
class SecretPathSet:

    LOUVRE_DOMAIN: str
    TOKEN_ENDPOINT: str
    CLIENT_ID_API: str
    CLIENT_SECRET_API: str


@dataclass
class SecretPathSets:

    secret_path_set: SecretPathSet
    secret_path_set_prod: Optional[SecretPathSet] = None

    def get_louvre_domain(self, using_production_images: bool = False) -> str:
        if not using_production_images:
            return self.secret_path_set.LOUVRE_DOMAIN
        if using_production_images and self.secret_path_set_prod:
            return self.secret_path_set_prod.LOUVRE_DOMAIN
        raise LouvreSecretError()

    def get_token_endpoint(self, using_production_images: bool = False) -> str:
        if not using_production_images:
            return self.secret_path_set.TOKEN_ENDPOINT
        if using_production_images and self.secret_path_set_prod:
            return self.secret_path_set_prod.TOKEN_ENDPOINT
        raise LouvreSecretError()

    def get_client_id_api(self, using_production_images: bool = False) -> str:
        if not using_production_images:
            return self.secret_path_set.CLIENT_ID_API
        if using_production_images and self.secret_path_set_prod:
            return self.secret_path_set_prod.CLIENT_ID_API
        raise LouvreSecretError()

    def get_client_secret_api(self,
                              using_production_images: bool = False) -> str:
        if not using_production_images:
            return self.secret_path_set.CLIENT_SECRET_API
        if using_production_images and self.secret_path_set_prod:
            return self.secret_path_set_prod.CLIENT_SECRET_API
        raise LouvreSecretError()

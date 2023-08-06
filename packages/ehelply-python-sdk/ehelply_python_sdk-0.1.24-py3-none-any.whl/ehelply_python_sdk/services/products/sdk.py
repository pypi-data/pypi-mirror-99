from .schemas import *
from ehelply_python_sdk.services.service_sdk_base import SDKBase


class ProductsSDK(SDKBase):
    def get_base_url(self) -> str:
        return super().get_base_url() + "/products"

    def get_docs_url(self) -> str:
        return super().get_docs_url()

    def get_service_version(self) -> str:
        return super().get_service_version()

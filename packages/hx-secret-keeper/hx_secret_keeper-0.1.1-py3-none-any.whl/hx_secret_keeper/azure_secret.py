from .base_secret import Secret


class AzureSecret(Secret):
    def retrieve_secret(self, service_name: str, env: str, cloud: str="aws", region_name: str="us-west-2"):
        raise NotImplementedError

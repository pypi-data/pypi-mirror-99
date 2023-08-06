import os

from .aws_secret import AWSSecret
from .azure_secret import AzureSecret


class SecretFactory(object):
    def get_secret_client(self):
        if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
            return AWSSecret()
        else:
            return AzureSecret()

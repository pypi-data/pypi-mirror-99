import base64
import json
import os
from botocore.exceptions import ClientError

import boto3
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig

from .base_secret import Secret

class AWSSecret(Secret):
    def __init__(self):
        # Create a Secrets Manager client
        session = boto3.session.Session()
        self.client = session.client(
            service_name="secretsmanager",
            region_name=os.environ.get("AWS_DEFAULT_REGION", "us-west-2")
        )
        # Create a cache
        self.cache = SecretCache(SecretCacheConfig(), self.client)


    def retrieve_secret(self, service_name: str, env: str, cloud: str="aws", region_name: str="us-west-2"):
        secret_name = f"{env}/{cloud}/{region_name}/{service_name}"
        try:
            # Get secret string from the cache
            secret_value_response = self.cache.get_secret_string(secret_name)

        except ClientError as e:
            raise e
        else:
            return json.loads(secret_value_response)

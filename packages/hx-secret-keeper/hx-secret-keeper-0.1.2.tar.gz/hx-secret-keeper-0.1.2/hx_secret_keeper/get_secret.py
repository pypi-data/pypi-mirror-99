from .secret_factory import SecretFactory

secret_client = None
def get_secret(service_name: str, env: str, cloud: str="aws", region: str="us-west-2"):
    """
    Function to retrieve secrets.

    Parameters:
    service_name (str): Resource for which the secret is required
    env (str): Can take one of "dev", "staging", "greenprod" or "blueprod" values
    cloud (str): Cloud Provider. Currently supports "aws" and "azure". Default: "aws"
    region (str): Cloud Provider Region. Default: "us-west-2"

    Returns:
    secret_value (json)
    """

    global secret_client
    if not secret_client:
        secret_client = SecretFactory().get_secret_client()

    return secret_client.retrieve_secret(service_name, env, cloud, region)

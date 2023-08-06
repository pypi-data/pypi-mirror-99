class Secret(object):
    def retrieve_secret(self, service_name: str, env: str, cloud: str, region_name: str):
        raise NotImplementedError()

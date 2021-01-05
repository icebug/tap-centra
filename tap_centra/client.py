import time
import requests
import singer
import zlib
import json
import base64


from tap_framework.client import BaseClient
from requests.auth import HTTPBasicAuth


LOGGER = singer.get_logger()


class CentraClient(BaseClient):
    def __init__(self, config):
        super().__init__(config)

        self.token = self.config.get("api_key")
        self.base_url = self.config.get("base_url")

    def get_authorization(self):
        pass

    def get_headers(self):
        headers = {
            "Content-Type": "application/json",
            "API-Authorization": self.token
        }

        return headers

    def make_request(self, path, method, base_backoff=45,
                     params=None, body=None):
        headers = self.get_headers()
        url = self.base_url + path

        LOGGER.info("Making {} request to {}".format(method, url))

        response = requests.request(
            method,
            url,
            headers=headers,
            params=params)

        if response.status_code == 429:
            LOGGER.info('Got a 429, sleeping for {} seconds and trying again'
                        .format(base_backoff))
            time.sleep(base_backoff)
            return self.make_request(url, method, base_backoff * 2, params, body)

        if response.status_code != 200:
            raise RuntimeError(response.text)

        return response.json()

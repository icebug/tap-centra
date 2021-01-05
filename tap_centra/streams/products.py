
from tap_centra.streams.base import BaseStream
import singer


class ProductsStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "products"
    KEY_PROPERTIES = ["sku"]

    def response_key(self):
        return "products"

    def sync_paginated(self, path, params):
        table = self.TABLE

        response = self.client.make_request(
            path, self.API_METHOD, params=params)
        transformed = self.get_stream_data(response)

        with singer.metrics.record_counter(endpoint=table) as counter:
            singer.write_records(table, transformed)
            counter.increment(len(transformed))


    @property
    def path(self):
        return "/products"

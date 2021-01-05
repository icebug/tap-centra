
from tap_centra.streams.base import BaseStream
from tap_centra.cache import stream_cache
import singer


class StockStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "stock"
    KEY_PROPERTIES = ["sizeSku"]

    def response_key(self):
        return "data"

    def get_params(self):
        return {}

    def sync_paginated(self, path, params):
        table = self.TABLE

        response = self.client.make_request(
            path, self.API_METHOD, params=params)
        transformed = self.get_stream_data(response)

        with singer.metrics.record_counter(endpoint=table) as counter:
            singer.write_records(table, transformed)
            counter.increment(len(transformed))

        if self.CACHE:
            stream_cache[table].extend(transformed)

    def get_stream_data(self, response):
        transformed = []

        for record in response['products']:
            record = self.transform_record(record)
            transformed.append(record)

        return transformed

    @property
    def path(self):
        return "/stock"

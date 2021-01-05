import singer
import singer.utils
import singer.metrics
import datetime

from tap_centra.state import incorporate, save_state

from tap_framework.streams import BaseStream as base
from tap_centra.cache import stream_cache


LOGGER = singer.get_logger()


class BaseStream(base):
    KEY_PROPERTIES = ["OrderId, CustomerId", "sku", "returnId"]
    CACHE = False
    ORDER_LIMIT = 200

    def get_params(self):
        params = {
            "limit": self.ORDER_LIMIT,
            "offset": 0
        }

        return params

    def sync_paginated(self, path, params):
        table = self.TABLE
        order_limit = self.ORDER_LIMIT
        offset = 0

        while True:
            params['offset'] = offset
            response = self.client.make_request(
                path, self.API_METHOD, params=params)
            transformed = self.get_stream_data(response)

            with singer.metrics.record_counter(endpoint=table) as counter:
                singer.write_records(table, transformed)
                counter.increment(len(transformed))

            if self.CACHE:
                stream_cache[table].extend(transformed)

            data = response.get(self.response_key(), [])

            if len(data) < order_limit:
                break
            else:
                offset += len(data)
                LOGGER.info('Offset: ' + str(offset))

    def sync_data(self):
        table = self.TABLE
        LOGGER.info("Syncing data for {}".format(table))
        path = table
        params = self.get_params()
        self.sync_paginated(path, params)

        return self.state

    def get_stream_data(self, response):
        transformed = []

        for record in response[self.response_key()]:
            record = self.transform_record(record)
            transformed.append(record)

        return transformed

    def response_key(self):
        pass

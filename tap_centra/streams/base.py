import singer
import singer.utils
import singer.metrics
from datetime import datetime
from dateutil.parser import parse

from tap_centra.state import incorporate, save_state, get_last_record_value_for_table

from tap_framework.streams import BaseStream as base
from tap_centra.cache import stream_cache


LOGGER = singer.get_logger()


class BaseStream(base):
    KEY_PROPERTIES = ["OrderId, CustomerId", "sku", "returnId"]
    CACHE = False
    ORDER_LIMIT = 200

    def get_params(self, start_date, offset):
        params = {
            "limit": self.ORDER_LIMIT,
            "offset": offset,
            "newer_than": start_date
        }
        return params

    def sync_paginated(self, path):
        table = self.TABLE
        order_limit = self.ORDER_LIMIT
        offset = 0

        date = get_last_record_value_for_table(self.state, table)
        if date is None:
            date = parse(self.config.get('start_date'))
        LOGGER.info('Syncing data from {}'.format(date.isoformat()))

        while True:
            params = self.get_params(date, offset)

            response = self.client.make_request(path, self.API_METHOD, params=params)
            transformed = self.get_stream_data(response)

            with singer.metrics.record_counter(endpoint=table) as counter:
                singer.write_records(table, transformed)
                counter.increment(len(transformed))

            if self.CACHE:
                stream_cache[table].extend(transformed)

            data = response.get(self.response_key(), [])
            last_record_date = self.get_last_record_date(data)

            if len(data) < order_limit:
                break
            else:
                offset += len(data)
                LOGGER.info('Offset: ' + str(offset))

            self.state = incorporate(self.state, table, 'last_record', last_record_date)
            save_state(self.state)

    def sync_data(self):
        table = self.TABLE
        LOGGER.info("Syncing data for {}".format(table))

        path = table
        self.sync_paginated(path)

        return self.state

    def get_stream_data(self, response):
        transformed = []

        for record in response[self.response_key()]:
            record = self.transform_record(record)
            record['reportDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transformed.append(record)

        return transformed

    def response_key(self):
        pass

    def get_last_record_date(self, data):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

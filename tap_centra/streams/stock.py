
from tap_centra.streams.base import BaseStream
from tap_centra.state import incorporate, save_state, get_last_record_value_for_table
from dateutil.parser import parse
from datetime import datetime
import singer

LOGGER = singer.get_logger()


class StockStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "stock"
    KEY_PROPERTIES = ["sizeSku"]

    def response_key(self):
        return "data"

    def sync_data(self):
        table = self.TABLE
        LOGGER.info("Syncing data for {}".format(table))

        path = table

        date = get_last_record_value_for_table(self.state, table)
        if date is None:
            date = parse(self.config.get('start_date'))
        LOGGER.info('Syncing data from {}'.format(date.isoformat()))

        response = self.client.make_request(path, self.API_METHOD)
        transformed = self.get_stream_data(response)

        with singer.metrics.record_counter(endpoint=table) as counter:
            singer.write_records(table, transformed)
            counter.increment(len(transformed))

        return self.state

    def get_stream_data(self, response):
        transformed = []

        for record in response['products']:
            record = self.transform_record(record)
            record['reportDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transformed.append(record)

        return transformed

    @property
    def path(self):
        return "/stock"


from tap_centra.streams.base import BaseStream
import singer
from tap_centra.state import incorporate, save_state, get_last_record_value_for_table
from dateutil.parser import parse

LOGGER = singer.get_logger()


class ProductsStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "products"
    KEY_PROPERTIES = ["sku"]

    def response_key(self):
        return "products"

    def get_last_record_date(self, data):
        return max([d.get('createdAt') for d in data])

    def get_params(self, start_date):
        params = {
            "modified": start_date
        }
        return params

    def sync_data(self):
        table = self.TABLE
        LOGGER.info("Syncing data for {}".format(table))

        path = table

        date = get_last_record_value_for_table(self.state, table)
        if date is None:
            date = parse(self.config.get('start_date'))
        LOGGER.info('Syncing data from {}'.format(date.isoformat()))

        params = self.get_params(date)

        response = self.client.make_request(path, self.API_METHOD, params=params)
        transformed = self.get_stream_data(response)

        with singer.metrics.record_counter(endpoint=table) as counter:
            singer.write_records(table, transformed)
            counter.increment(len(transformed))

        data = response.get(self.response_key(), [])
        if len(data) == 0:
            last_record_date = date
        else:
            last_record_date = self.get_last_record_date(data)

        self.state = incorporate(self.state, table, 'last_record', last_record_date)
        save_state(self.state)

        return self.state

    @property
    def path(self):
        return "/products"
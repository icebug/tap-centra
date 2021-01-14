
from tap_centra.streams.base import BaseStream
import singer

LOGGER = singer.get_logger()


class OrdersStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "orders"
    KEY_PROPERTIES = ["orderId"]
    ORDER_LIMIT = 5000

    def response_key(self):
        return "orders"

    def get_last_record_date(self, data):
        return data[-1].get('orderDate')

    @property
    def path(self):
        return "/orders"

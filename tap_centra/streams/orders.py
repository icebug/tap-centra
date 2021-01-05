
from tap_centra.streams.base import BaseStream
import singer

LOGGER = singer.get_logger()


class OrdersStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "orders"
    KEY_PROPERTIES = ["orderId"]
    ORDER_LIMIT = 1000

    def response_key(self):
        return "orders"

    @property
    def path(self):
        return "/orders"

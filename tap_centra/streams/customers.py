
from tap_centra.streams.base import BaseStream
import singer


class CustomersStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "customers"
    KEY_PROPERTIES = ["customerId"]
    ORDER_LIMIT = 200

    def response_key(self):
        return "customers"

    def get_params(self, start_date, offset):
        params = {
            "limit": self.ORDER_LIMIT,
            "offset": offset,
            "modified": start_date
        }
        return params

    @property
    def path(self):
        return "/customers"

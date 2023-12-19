from tap_centra.streams.base import BaseStream
from datetime import datetime, timedelta
import singer
import hashlib


LOGGER = singer.get_logger()


class OrdersStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "orders"
    KEY_PROPERTIES = ["orderId"]
    ORDER_LIMIT = 5000

    def response_key(self):
        return "orders"

    def get_params(self, start_date, offset):
        # Select min of start_date and current_date minus seven days
        # to ensure we get updates on recent orders
        start_date = min(start_date, datetime.now() - timedelta(days=7))
        formatted_start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        params = {"limit": self.ORDER_LIMIT, "offset": offset, "newer_than": formatted_start_date}
        return params

    def get_last_record_date(self, data):
        return data[-1].get("orderDate")

    def get_stream_data(self, response):
        transformed = []
        if response["status"] == "ok":
            for record in response[self.response_key()]:
                record = self.transform_record(record)
                record["reportDate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                record["emailHash"] = hashlib.md5(
                    record["deliveryEmail"].encode()
                ).hexdigest()
                del record["deliveryEmail"]
                transformed.append(record)

        return transformed

    @property
    def path(self):
        return "/orders"


from tap_centra.streams.base import BaseStream
import singer


class ReturnsStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "returns"
    KEY_PROPERTIES = ["returnId"]
    ORDER_LIMIT = 200

    def response_key(self):
        return "returns"

    @property
    def path(self):
        return "/returns"

    def get_last_record_date(self, data):
        return data[0].get('date')

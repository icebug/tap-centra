from tap_centra.streams.orders import OrdersStream
from tap_centra.streams.personal_information import PersonalInformationStream
from tap_centra.streams.products import ProductsStream
from tap_centra.streams.returns import ReturnsStream
from tap_centra.streams.stock import StockStream

AVAILABLE_STREAMS = [
    OrdersStream,
    PersonalInformationStream,
    ProductsStream,
    ReturnsStream,
    StockStream,
]

__all__ = [
    "OrdersStream",
    "PersonalInformationStream",
    "ProductsStream",
    "ReturnsStream",
    "StockStream",
]

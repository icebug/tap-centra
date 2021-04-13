from tap_centra.streams.orders import OrdersStream
from tap_centra.streams.customers import CustomersStream
from tap_centra.streams.products import ProductsStream
from tap_centra.streams.returns import ReturnsStream
from tap_centra.streams.stock import StockStream

AVAILABLE_STREAMS = [
    OrdersStream,
    # CustomersStream,
    ProductsStream,
    ReturnsStream,
    StockStream,
]

__all__ = [
    "OrdersStream",
    # "CustomersStream",
    "ProductsStream",
    "ReturnsStream",
    "StockStream",
]

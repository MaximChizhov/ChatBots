from .handler import Handler
from .message_start import MessageStart
from .database_logger import DbLogger
from .ensure_user_exists import EnsureUserExists
from .pizza_selection import PizzaSelection
from .pizza_size import PizzaSize
from .pizza_drinks import PizzaDrinks
from .order_approval import OrderApproval

def get_handlers() -> list[Handler]:
    return [
        DbLogger(),
        EnsureUserExists(),
        MessageStart(),
        PizzaSelection(),
        PizzaSize(),
        PizzaDrinks(),
        OrderApproval()
    ]
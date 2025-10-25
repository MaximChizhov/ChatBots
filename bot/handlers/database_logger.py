from .handler import *
from bot.database_client import persist_update


class DbLogger(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        return True

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        persist_update([update])
        return HandlerStatus.CONTINUE

from bot.handler import Handler
from bot.database_client import persists_updates


class DbLogger(Handler):
    def can_handle(self, update: dict) -> bool:
        return True

    def handle(self, update: dict) -> bool:
        persists_updates([update])
        return True

from bot.handler import Handler

class Dispatcher:
    def __init__(self):
        self._handlers: list[Handler] = []

    def add_handler(self, *handlers: list[Handler]) -> None:
        for handler in handlers:
            self._handlers.append(handler)

    def dispatch(self, update: dict) -> None:
        print("[D] handlers queue:", [type(h).__name__ for h in self._handlers])
        for handler in self._handlers:
            if handler.can_handle(update):
                print(f"[D] {type(handler).__name__}.can_handle = True")
                signal = handler.handle(update)
                print(f"[D] {type(handler).__name__}.handle returned {signal}")
                if not signal:
                    break
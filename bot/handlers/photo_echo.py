from bot.handler import Handler
import bot.telegram_client as tg


class PhotoEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "photo" in update["message"]

    def handle(self, update: dict) -> bool:
        # берём самый большой файл (последний в списке photo)
        file_id = update["message"]["photo"][-1]["file_id"]
        chat_id = update["message"]["chat"]["id"]
        tg.sendPhoto(chat_id=chat_id, photo_id=file_id)
        return False
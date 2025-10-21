from bot.handler import Handler
import bot.telegram_client as tg


class StickerEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "sticker" in update["message"]

    def handle(self, update: dict) -> bool:
        sticker_id = update["message"]["sticker"]["file_id"]
        chat_id = update["message"]["chat"]["id"]
        tg.sendSticker(chat_id=chat_id, sticker_id=sticker_id)
        return False
import bot.telegram_client as tg
import bot.database_client as db
from bot.handlers.handler import *
import json



class PizzaSize(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_SIZE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("size_")

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        size_mapping = {
            "size_small": "S (25cm)",
            "size_medium": "M (30cm)",
            "size_large": "L (35cm)",
            "size_xl": "XL (40cm)",
        }

        pizza_size = size_mapping.get(callback_data)
        data["pizza_size"] = pizza_size
        db.update_user_order_json(telegram_id, data)
        db.update_user_state(telegram_id, "WAIT_FOR_DRINKS")

        tg.answerCallbackQuery(update["callback_query"]["id"])

        tg.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        tg.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="Выберите напиток",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Кока Кола", "callback_data": "drink_coca_cola"},
                            {"text": "Пепси", "callback_data": "drink_pepsi"},
                        ],
                        [
                            {
                                "text": "Апельсиновый фреш",
                                "callback_data": "drink_orange_fresh",
                            },
                            {
                                "text": "Мохито",
                                "callback_data": "drink_mojito",
                            },
                        ],
                        [
                            {"text": "Вода", "callback_data": "drink_water"},
                            {"text": "Чай со льдом", "callback_data": "drink_iced_tea"},
                        ],
                        [
                            {"text": "Ничего", "callback_data": "drink_none"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP

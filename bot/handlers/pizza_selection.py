import bot.telegram_client as tg
import bot.database_client as db
from bot.handlers.handler import *
import json



class PizzaSelection(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_NAME":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        pizza_mapping = {
            "pizza_margherita": "Маргарита",
            "pizza_pepperoni": "Пепперони",
            "pizza_quattro_formaggi": "Четыре сыра",
            "pizza_hawaiian": "Гавайская",
            "pizza_diavola": "Диабло",
            "pizza_carbonara": "Карбонара"
        }

        pizza_name = pizza_mapping.get(callback_data, "Unknown")
        db.update_user_order_json(telegram_id, {"pizza_name": pizza_name})
        db.update_user_state(telegram_id, "WAIT_FOR_PIZZA_SIZE")
        tg.answerCallbackQuery(update["callback_query"]["id"])
        tg.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )
        tg.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="Выберите размер пиццы",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "S (25cm)", "callback_data": "size_small"},
                            {"text": "M (30cm)", "callback_data": "size_medium"},
                        ],
                        [
                            {"text": "L (35cm)", "callback_data": "size_large"},
                            {"text": "XL (40cm)", "callback_data": "size_xl"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
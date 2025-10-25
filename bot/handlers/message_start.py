import bot.telegram_client as tg
import bot.database_client
from bot.handlers.handler import *
import json


class MessageStart(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        return (
            "message" in update
            and "text" in update["message"]
            and update["message"]["text"] == "/start"
        )

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]

        bot.database_client.clear_user_state_and_order(telegram_id)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

        tg.sendMessage(
            chat_id=update["message"]["chat"]["id"],
            text="🍕 Добро пожаловать в Pizza shop!",
            reply_markup=json.dumps({"remove_keyboard": True}),
        )

        tg.sendMessage(
            chat_id=update["message"]["chat"]["id"],
            text="Выберите пиццу",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {
                                "text": "Маргарита",
                                "callback_data": "pizza_margherita"
                            },
                            {
                                "text": "Пепперони",
                                "callback_data": "pizza_pepperoni"
                            },
                        ],
                        [
                            {
                                "text": "Четыре сыра",
                                "callback_data": "pizza_quattro_formaggi",
                            },
                            {
                                "text": "Гавайская",
                                "callback_data": "pizza_hawaiian",
                            },
                        ],
                        [
                            {
                                "text": "Диабло",
                                "callback_data": "pizza_diavola"
                            },
                            {
                                "text": "Карбонара",
                                "callback_data": "pizza_carbonara"
                            },
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP

import json

import bot.telegram_client as tg
from bot.database_client import clear_user_state_and_order, update_user_state
from bot.handlers.handler import *

class OrderApproval(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["order_approve", "order_restart"]

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        tg.answerCallbackQuery(update["callback_query"]["id"])
        tg.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        if callback_data == "order_approve":
            update_user_state(telegram_id, "ORDER_FINISHED")

            pizza_name = data.get("pizza_name", "Unknown")
            pizza_size = data.get("pizza_size", "Unknown")
            drink = data.get("drink", "Unknown")

            order_confirmation = f"""✅ **Заказ сформирован!**
🍕 **Ваш заказ:**
• Пицца: {pizza_name}
• Размер: {pizza_size}
• Напиток: {drink}

Спасибо за заказ! Ваша пицца скоро будет готова.

Отправьте /start, чтобы сделать еще один заказ."""

            # Send order confirmation message
            tg.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text=order_confirmation,
                parse_mode="Markdown",
            )

        elif callback_data == "order_restart":
            clear_user_state_and_order(telegram_id)

            # Update user state to wait for pizza selection
            update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

            # Send pizza selection message with inline keyboard
            tg.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
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
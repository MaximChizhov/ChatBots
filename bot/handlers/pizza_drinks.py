import bot.telegram_client as tg
import bot.database_client as db
from bot.handlers.handler import *
import json


class PizzaDrinks(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_DRINKS":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        # Extract drink name from callback data (remove 'drink_' prefix)
        drink_mapping = {
            "drink_coca_cola": "Кока Кола",
            "drink_pepsi": "Пепси",
            "drink_orange_fresh": "Апельсиновый фреш",
            "drink_mojito": "Мохито",
            "drink_water": "Вода",
            "drink_iced_tea": "Чай со льдом",
            "drink_none": "Ничего",
        }
        selected_drink = drink_mapping.get(callback_data)

        data["drink"] = selected_drink

        db.update_user_order_json(telegram_id, data)
        db.update_user_state(telegram_id, "WAIT_FOR_ORDER_APPROVE")
        tg.answerCallbackQuery(update["callback_query"]["id"])

        tg.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        # Create order summary message
        pizza_name = data.get("pizza_name", "Unknown")
        pizza_size = data.get("pizza_size", "Unknown")
        drink = data.get("drink", "Unknown")

        order_summary = f"""🍕 **Ваш заказ:**

**Пицца:** {pizza_name}
**Размер:** {pizza_size}
**Напиток:** {drink}

Всё верно?"""

        tg.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=order_summary,
            parse_mode="Markdown",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "✅ Ok", "callback_data": "order_approve"},
                            {
                                "text": "🔄 Начать снова",
                                "callback_data": "order_restart",
                            },
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
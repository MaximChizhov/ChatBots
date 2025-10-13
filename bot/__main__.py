import bot.database_client
import bot.telegram_client
import time

def main() -> None:
    next_update_offset = 0
    try:
        while True:
            updates = bot.telegram_client.getUpdates(next_update_offset)
            bot.database_client.persists_updates(updates)

            for update in updates:
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")

                # Если пришёл текст
                if "text" in message:
                    text = message["text"]
                    bot.telegram_client.sendMessage(chat_id=chat_id, text=text)

                # Если пришло фото
                elif "photo" in message:
                    photo_array = message["photo"]
                    photo = photo_array[-1]
                    photo_id=photo["file_id"]
                    bot.telegram_client.sendPhoto(chat_id=chat_id, photo_id=photo_id)

                # Если пришёл стикер
                elif "sticker" in message:
                    sticker_id = message["sticker"]["file_id"]
                    bot.telegram_client.sendSticker(chat_id=chat_id, sticker_id=sticker_id)

                # Всё остальное игнорируем
                else:
                    bot.telegram_client.sendMessage(chat_id=chat_id, text="Я понимаю только текст и стикеры 😊")

                print("@", end="", flush=True)
                next_update_offset = max(next_update_offset, update["update_id"] + 1)

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBye!")



if __name__ == "__main__":
    main()
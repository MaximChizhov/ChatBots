from bot.dispatcher import Dispatcher
from bot.handlers import MessageEcho, PhotoEcho, StickerEcho, DbLogger
from bot.long_polling import start_long_polling


def main() -> None:
    try:
        dispatcher = Dispatcher()
        dispatcher.add_handler(DbLogger(), MessageEcho(), PhotoEcho(), StickerEcho())
        start_long_polling(dispatcher)

    except KeyboardInterrupt:
        print("\nBye!")

if __name__ == "__main__":
    main()

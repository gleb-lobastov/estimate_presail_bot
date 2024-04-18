import traceback


class BotError(Exception):
    def __init__(self, message="Ошибка бота"):
        self.message = message
        super().__init__(self.message)


def handle_errors(handler):
    async def wrapper(message):
        try:
            return await handler(message)
        except BotError as e:
            print("\n\n Известное исключение \n\n" + traceback.format_exc() + "\n\n")
            await message.answer(text=str(e))
        except Exception:
            print("\n\n Неизвестная ошибка \n\n" + traceback.format_exc() + "\n\n")
            await message.answer(text="Неизвестная ошибка")

    return wrapper

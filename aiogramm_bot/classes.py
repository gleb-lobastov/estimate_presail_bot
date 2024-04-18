import io
import traceback

from aiogram import types

from scenario.abc import Document, Message
from utils.telegram import adapt_answer

from .bot import bot


class AiogramScenarioRunner:
    """
    Класс `AiogramScenarioRunner` описывает объект для контроля сценариями пользовательского ввода

    Attributes:
        _command: Название команды запустившей процесс
        _gen: Генератор для выполнения асинхронных шагов.
        _filter: Фильтр для следующего сообщения ожидаемого сценарием

    Methods:
        active(): Проверяет, активен ли сценарий.
        command(): Возвращает название команды запустившей сценарий
        start(scenario, message): Начинает выполнение сценария.
        step(message): Выполняет следующий шаг в сценарии.
        stop(): Останавливает выполнение сценария и очищает состояние.
    """

    def __init__(self) -> None:
        self._command = None
        self._gen = None
        self._filter = None

    @property
    def active(self) -> bool:
        return self._gen is not None

    @property
    def command(self) -> str:
        return self._command.replace("/", "")

    async def play(self, scenario, message) -> None:
        self._command = message.text
        self._gen = scenario(AiogramMessage(message))
        self._filter = await self._gen.__anext__()

    async def step(self, message) -> None:
        if not hasattr(self._filter, "resolve") or self._filter.resolve(message):
            try:
                self._filter = await self._gen.asend(AiogramMessage(message))
            except StopAsyncIteration as e:
                self.stop()
                await message.answer("Обработка команды завершена")
            except Exception as e:
                self.stop()
                print("\n\n Неизвестная ошибка \n\n" + str(e) + "\n\n" + traceback.format_exc() + "\n\n")
                await message.answer("Произошла ошибка в ходе выполнения команды")

    def stop(self) -> None:
        self._command = None
        self._gen = None
        self._filter = None


class AiogramMessage(Message):
    """
       Класс `AiogramMessage` реализует интерфейс Message определенный в модуле scenario
       Класс используется, чтобы сценарии знали как взаимодействовать с сообщениями aiogramm
    """

    def __init__(self, message: types.Message):
        self._message = message

    @property
    def text(self):
        return self._message.text

    @property
    def document(self):
        return AiogramDocument(self._message.document) if self._message.document else None

    async def answer(self, text):
        return await adapt_answer(self._message.answer, text=text)


class AiogramDocument(Document):
    """
       Класс `AiogramDocument` реализует интерфейс Document определенный в модуле scenario
       Класс используется, чтобы сценарии знали как взаимодействовать с аттачментами aiogramm
    """

    def __init__(self, document):
        self._document = document

    @property
    def filename(self):
        return self._document.file_name

    async def get_content(self):
        file_in_io = io.BytesIO()
        await bot.download(file=self._document.file_id, destination=file_in_io)
        return file_in_io

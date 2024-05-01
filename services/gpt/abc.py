from abc import ABC, abstractmethod
import aiohttp

from .consts import DEFAULT_SYSTEM_MESSAGE


class AbstractGPT(ABC):
    """
    Абстрактный класс для взаимодействия с LLM моделями
    1. Определяет интерфейс взаимодействия
    2. Реализующий интерфейс асинхронного менеджера контекста для работы с aiohttp

    Attributes:
        SESSION_REQUIRED: Флаг класса, указывающий, требуется ли сеанс клиента aiohttp.

    Methods:
        prompt(): Абстрактный метод для отправки запроса к модели

    """
    SESSION_REQUIRED = True
    _system_message = DEFAULT_SYSTEM_MESSAGE

    @property
    def system_message(self):
        return self._system_message

    def __init__(self, *, system_message="", **kwargs) -> None:
        self._session = aiohttp.ClientSession() if type(self).SESSION_REQUIRED else None
        if system_message:
            self._system_message = system_message

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        if type(self).SESSION_REQUIRED:
            await self._session.close()

    @abstractmethod
    async def prompt(self, text):
        pass

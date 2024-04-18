from abc import ABC, abstractmethod
import aiohttp


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

    def __init__(self) -> None:
        self._session = aiohttp.ClientSession() if type(self).SESSION_REQUIRED else None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        if type(self).SESSION_REQUIRED:
            await self._session.close()

    @abstractmethod
    async def prompt(self, text):
        pass

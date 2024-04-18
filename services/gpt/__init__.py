from .giga_chat import GigaChatGPT
from .manual_prompt import ManualPrompt
from .chat_gpt import OpenAIChatGPT3, OpenAIChatGPT4

AVAILABLE_MODELS = {
    "gpt3": OpenAIChatGPT3,
    "gpt4": OpenAIChatGPT4,
    "giga": GigaChatGPT,
    "manual": ManualPrompt,
}

MODEL_DESCRIPTIONS = {
    "gpt3": "ChatGPT v3.5",
    "gpt4": "ChatGPT v4",
    "giga": "GigaChat от Сбера",
    "manual": "Ручное копирование из бота в интерфейс LLM",
}

DEFAULT_MODEL = OpenAIChatGPT4


class GPTController:
    """
    Контроллер для выбора LLM модели

    Attributes:
        _Model: Текущая выбранная модель.

    Methods:
        select(model_name): Выбор модель из AVAILABLE_MODELS по имени
        current(): Возвращает текущую выбранную модель.
    """
    def __init__(self):
        self._Model = DEFAULT_MODEL

    def select(self, model_name):
        self._Model = AVAILABLE_MODELS.get(model_name)
        return self._Model is not None

    @property
    def current(self):
        return self._Model


gpt_controller = GPTController()

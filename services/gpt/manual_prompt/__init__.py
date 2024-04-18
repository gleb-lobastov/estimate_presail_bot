from ..abc import AbstractGPT


class ManualPrompt(AbstractGPT):
    SESSION_REQUIRED = False

    def __init__(self, *, answer, **kwargs):
        super().__init__()
        self._answer = answer

    async def prompt(self, text):
        await self._answer("Задайте промпт GPT самостоятельно и введите полученный ответ:")
        await self._answer(text)

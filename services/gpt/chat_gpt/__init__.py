from openai import OpenAI
from config import OPENAI_TOKEN
from ..abc import AbstractGPT


class OpenAIChatGPT(AbstractGPT):
    SESSION_REQUIRED = False

    def __init__(self, *, model="gpt-3.5-turbo-16k", **kwargs):
        super().__init__(**kwargs)
        self._model = model
        self._client = OpenAI(api_key=OPENAI_TOKEN)

    async def prompt(self, text):
        completion = self._client.chat.completions.create(
            model=self._model,
            temperature=0.3,
            messages=[
                {"role": "system", "content": self._system_message},
                {"role": "user", "content": text}
            ]
        )
        reply = completion.choices[0].message.content

        return reply


class OpenAIChatGPT3(OpenAIChatGPT):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, model="gpt-3.5-turbo-16k")


class OpenAIChatGPT4(OpenAIChatGPT):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, model="gpt-4-turbo")

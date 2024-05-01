from uuid import uuid4
from config import GIGACHAT_TOKEN
from ..abc import AbstractGPT

SCOPE = "GIGACHAT_API_PERS"
OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


class GigaChatGPT(AbstractGPT):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._token = None

    async def get_token(self):
        if self._token:
            return self._token

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid4()),
            'Authorization': f'Basic {GIGACHAT_TOKEN}'
        }
        data = {
            'scope': SCOPE,
            'grant_type': 'client_credentials',
        }
        async with self._session.request("POST", OAUTH_URL, data=data, headers=headers,
                                         verify_ssl=False) as response:

            if response.text:
                data = await response.json()
                self._token = data.get("access_token")
                return self._token
            else:
                raise Exception(
                    "Ошибка: не удалось получить токен. Код ответа сервера: " + str(response.status_code))

    async def prompt(self, text):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + await self.get_token(),
        }
        data = {
            "model": "GigaChat:latest",
            "messages": [
                {"role": "system", "content": self._system_message},
                {"role": "user", "content": text},
            ],
            "temperature": 0.7
        }
        async with self._session.request("POST", API_URL, json=data, headers=headers, verify_ssl=False) as response:
            data = await response.json()

            return data["choices"][0]["message"]["content"]

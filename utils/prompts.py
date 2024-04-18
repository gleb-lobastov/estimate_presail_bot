import yaml

from utils.errors import BotError


class Prompt:
    """
    Класс для подстановки параметров в загруженный промпт
    """

    def __init__(self, prompt):
        self.prompt = prompt

    def exec(self, data):
        # todo: тут было бы полезно реализовать поддержку отправки цепочки сообщений, в т.ч. с ролью System
        return self.prompt.replace("{{document}}", data)


class Prompts:
    """
    Класс для загрузки и доступа к набору промптов
    """

    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            prompts = yaml.safe_load(file)
        self.prompts = prompts

    def __getitem__(self, name):
        if name in self.prompts:
            return Prompt(self.prompts[name])
        raise BotError(f'Неизвестный промпт {name}')

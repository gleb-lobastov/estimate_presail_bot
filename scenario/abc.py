from abc import ABC, abstractmethod


class Document(ABC):

    @property
    @abstractmethod
    def filename(self):
        pass

    @abstractmethod
    def get_content(self):
        pass


class Message(ABC):

    @property
    @abstractmethod
    def text(self):
        pass

    @property
    @abstractmethod
    def document(self) -> Document:
        pass

    @abstractmethod
    async def answer(self, text):
        pass

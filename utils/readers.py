import io
import fitz
from external.pymupdf_rag import to_markdown
from utils.errors import BotError


def read_pdf(stream):
    try:
        doc = fitz.open(stream=stream)
        return to_markdown(doc)
    except Exception as e:
        raise BotError("Ошибка чтения pdf файла: " + str(e))


def read_md(stream):
    try:
        wrapper = io.TextIOWrapper(stream, encoding='utf-8')
        return wrapper.read()
    except Exception as e:
        raise BotError("Ошибка чтения md файла: " + str(e))

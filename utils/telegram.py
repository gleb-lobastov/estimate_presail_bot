import time
from functools import reduce
from utils.text import find_nearest_split
from utils.format import russian_plural

RESERVED_SYMBOLS = 100
MAX_MESSAGE_LENGTH = 4096 - RESERVED_SYMBOLS
SEEK_DISTANCE_LEN = 100
MAX_CHUNKS_COUNT = 10


async def adapt_answer(answer, text):
    """
    Адаптирует ответ бота к требованиям телеграма:
    - разбивает ответ на чанки не превышающие ограничения телеграма по количеству символов
    - отправляет чанки отдельными сообщениями
    """
    chunks = split_to_chunks(text)

    if len(chunks) == 1:
        await answer(text)
        return

    if len(chunks) > MAX_CHUNKS_COUNT:
        total_len = reduce(lambda total, y: total + len(y), chunks, 0)
        await answer(f'Система сформировала слишком большой ответ, будут выведены первые {total_len} {russian_plural(
            total_len,
            ["символ", "символа", "символов"]
        )}')
        chunks = chunks[:10]

    for index, chunk in enumerate(chunks):
        await answer(f'Сообщение {index + 1}/{len(chunks)}\n{chunk}\n\n')
        time.sleep(0.1)


def split_to_chunks(text, max_message_length=MAX_MESSAGE_LENGTH, seek_distance_len=SEEK_DISTANCE_LEN,
                    max_chunks_count=MAX_CHUNKS_COUNT):
    if not text:
        return

    tail = text
    chunks = []
    while len(tail):
        str_return_pos = find_nearest_split(tail, max_message_length, seek_distance_len)
        shift = 1 if str_return_pos < len(tail) and tail[str_return_pos] in ["\n", " "] else 0
        head, tail = tail[:str_return_pos], tail[str_return_pos + shift:]
        chunks.append(head)
        if len(chunks) > max_chunks_count + 1:
            break

    return chunks

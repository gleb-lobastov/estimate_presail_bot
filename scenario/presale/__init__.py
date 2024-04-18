from aiogram import F, types

from functools import reduce

from utils.prompts import Prompts
from utils.errors import BotError
from utils.readers import read_md, read_pdf
from utils.format import russian_plural
from services.gpt import gpt_controller

from .transform import (
    semantic_split,
    prepare_for_clean_prompt,
    clean,
    aggregate,
    disaggregate,
    summarize_tasks,
    content_to_estimate
)

MAX_SECTIONS_COUNT = 7
# fixme: применены фильтры из aiogramm, а сценарии не должны зависеть от типа бота
TEXT_OR_DOC_INPUT_TYPE = F.content_type.in_({types.ContentType.TEXT, types.ContentType.DOCUMENT})
TEXT_INPUT_TYPE = F.content_type == types.ContentType.TEXT

prompts = Prompts("./scenario/presale/prompts.yml")


async def scenario_presale(message):
    """
    Сценарий оценки трудозатрат на фронтенд-разработку с использованием LLM модели.

    Arguments:
        message: Сообщение пользователя

    Return:
        None

    Description:
        1. Сценарий запрашивает у пользователя техническое задание в формате markdown или pdf
        2. Данные пользовательского ввода преобразуются в md формат
        3. Выделяются семантически значимые блоки текста
        4. Размер блоков адаптируется под ограничения LLM по количеству токенов
        5. LLM по отдельности оценивает трудозатраты на каждый раздел
        6. LLM аггрегирует оценки
        7. Скрипт считает общие затраты

        Конструкция await gpt.prompt(prompt) or (yield TEXT_INPUT_TYPE).text используется для особого случая,
        когда вместо программного запроса к LLM пользователю предлагается выполнить запрос вручную
        Конструкция yield заставляет сценарий остановиться и ждать следующего пользовательского ввода,
        соответствующего переданным фильтрам.

        К сожалению не нашел способов более элегантно обработать эту особенность, так, чтобы не было излишнего кода.
        yield from мог бы быть хорош для передачи управления в саб-генератор, но он не поддерживается
        в асинхронных генераторах https://peps.python.org/pep-0525/#asynchronous-yield-from
        конструкция for v in sub_generator(): yield v не позволяет использовать send для передачи значения в
        саб-генератор
    """
    async with (gpt_controller.current(answer=message.answer) as gpt):

        await message.answer("Пришлите техническое задание в формате md или pdf, либо сообщением")
        user_input = yield TEXT_OR_DOC_INPUT_TYPE
        if user_input.document:
            extension = user_input.document.filename.split(".")[-1]
            if extension not in ["pdf", "md"]:
                raise BotError(f'Не поддерживаемый тип документа {extension}. Загрузите файл в формате pdf или md')
            raw_document = to_md(await user_input.document.get_content(), extension)
        else:
            raw_document = user_input.text

        sections = semantic_split(raw_document)
        titles_count = reduce(lambda count, section: count + 1 if section["title"] else count, sections, 0)

        if titles_count > 1:
            await message.answer("Выполняется запрос на уточнение структуры документа")
            prompt = prompts["clean_titles"].exec(prepare_for_clean_prompt(sections))
            resp_clean_titles = await gpt.prompt(prompt) or (yield TEXT_INPUT_TYPE).text

            await message.answer(f'Структура документа: {resp_clean_titles}')
            sections = clean(sections, resp_clean_titles)

        sections = [*aggregate(disaggregate(sections))]

        if len(sections) > MAX_SECTIONS_COUNT:
            sections = sections[:MAX_SECTIONS_COUNT]
            await message.answer(
                f'В связи с ограничениями бота, будет оценено только первые {MAX_SECTIONS_COUNT}'
                + f'блоков из {len(sections)} (~20к символов)'
            )

        resps_evaluated_tasks = ""
        for section in sections:
            if not any(char.isalpha() for char in section["content"]):
                continue
            prompt = prompts["evaluate_section"].exec(content_to_estimate(section))
            await message.answer(f'Выполняется запрос для раздела/разделов: {section["title"] or "Без заголовка"}\n')
            resp_evaluated_tasks = await gpt.prompt(prompt) or (yield TEXT_INPUT_TYPE).text
            await message.answer(f'Задачи: {resp_evaluated_tasks}')

            resps_evaluated_tasks += resp_evaluated_tasks + "\n"

        prompt = prompts["remove_dupes"].exec(resps_evaluated_tasks)
        await message.answer("Выполняется запрос на объединение задач разных разделов")
        resp_deduped_task = await gpt.prompt(prompt) or (yield TEXT_INPUT_TYPE).text

        await message.answer("Итоговый список задач:\n" + resp_deduped_task)
        evaluation_total = summarize_tasks(resp_deduped_task)

        await message.answer(
            f'Общая оценка: {evaluation_total} {russian_plural(
                evaluation_total,
                ["час", "часа", "часов"]
            )}'
        )


def to_md(content_stream, extension):
    content = None
    if extension == "pdf":
        return read_pdf(content_stream)
    elif extension == "md":
        content = read_md(content_stream)
    if not content:
        raise BotError("Пустой документ")
    return content

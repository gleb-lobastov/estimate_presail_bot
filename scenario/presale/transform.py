import re
from utils.text import find_nearest_split


def semantic_split(markdown):
    sections = []
    content_buffer = []

    markdown.replace("\n\n", "\n---\n")

    length = len(markdown)

    cursor = 0
    # читаем список снизу вверх, чтобы найденный заголовок можно было сразу соотнести с буфером и кешировать
    for line in reversed(markdown.split('\n')):
        line = line.strip()
        if not line:
            continue
        cursor += len(line)
        kind_of_line = resolve_kind(line)
        if kind_of_line not in ["title", "divider"]:
            content_buffer.append(line)

        if kind_of_line:
            sections.append({
                "pos": length - cursor,
                "title": line if kind_of_line == "title" else None,
                "content": "\n".join(reversed(content_buffer))
            })
            content_buffer = []
        cursor += 1  # Учитываем "/n", удаленную методом split

    if content_buffer:
        sections.append({
            "pos": 0,
            "title": None,
            "content": "\n".join(reversed(content_buffer))
        })

    return [*reversed(sections)]


MAX_SECTION_LEN = 3296
SEEK_DISTANCE_LEN = 296


def disaggregate(sections):
    """
    Разукрупняет слишком большие секции, с учетом семантики
    """
    for section in sections:
        tail = section["content"]
        if not len(tail):
            yield section  # для последующей агрегации заголовка
        total_pos = section["pos"]
        while len(tail) > 0:
            str_return_pos = find_nearest_split(tail, MAX_SECTION_LEN, SEEK_DISTANCE_LEN)
            head, tail = tail[:str_return_pos], tail[str_return_pos:]
            yield {"pos": total_pos, "title": section["title"], "content": head, "d": True}
            total_pos += str_return_pos


def aggregate(sections):
    """
    Объединяет маленькие секции для уменьшения количества запросов
    """
    content_to_aggregate = []
    title_to_aggregate = []
    last_pos = 0

    for section in sections:
        delta = section["pos"] - last_pos
        if delta > MAX_SECTION_LEN:
            yield agg_section(last_pos, title_to_aggregate, content_to_aggregate)
            content_to_aggregate = []
            title_to_aggregate = []
            last_pos = section["pos"]

        content_to_aggregate.append(section["content"])
        if section["title"]:
            title_to_aggregate.append(section["title"])

    if len(content_to_aggregate):
        yield agg_section(last_pos, title_to_aggregate, content_to_aggregate)


def agg_section(last_pos, title_to_aggregate, content_to_aggregate):
    return {
        "pos": last_pos,
        "title": ".".join(title_to_aggregate),
        "content": "\n".join(content_to_aggregate)
    }


def resolve_kind(line):
    """
        Грубо определяет семантику строки в md тексте

        Parameters:
            line (str): Строка текста

        Returns:
            str or None: Тип строки, если удалось его выделить по определенным признакам
                - "title" для заголовков
                - "divider" для раздела частей текста
                - "emphasis" для важного текста
                - "list" для списков
                - "colon" для строки начинающей список или объяснение
                - None для всех обычных строк
        """
    if line.startswith('#'):
        return "title"
    elif line.startswith('---'):
        return "divider"
    elif line.startswith('**'):
        return "emphasis"
    elif line.startswith('-'):
        return "list"
    elif line[0].isdigit():
        return "list"
    elif line.endswith(':'):
        return "colon"
    else:
        return None


def prepare_for_clean_prompt(sections):
    return "\n".join([
        f'{section["title"]}//>{section["pos"]}'
        for section in sections
        if section["title"]
    ])


def clean(sections, resp_clean_sections):
    """
    Заменяет изначальные заголовки уточненными
    """
    clean_titles = {}
    for line in resp_clean_sections.split("\n"):
        parts = line.split("//>")
        if len(parts) == 2:
            title, str_pos = parts
            clean_titles[str_pos.strip()] = title

    cleaned_sections = []
    for section in sections:
        clean_title = clean_titles.get(str(section["pos"]))
        cleaned_sections.append({**section, "title": clean_title})

    return cleaned_sections


MAX_TITLE_LENGTH = 100
MAX_TITLE_SEEK_DISTANCE = 20


def content_to_estimate(section):
    if not section["title"]:
        return section["content"]
    split_pos = find_nearest_split(
        section["title"],
        max_length=MAX_TITLE_LENGTH,
        max_seek_distance=MAX_TITLE_SEEK_DISTANCE
    )
    adapted_title = section["title"][0:split_pos]
    return adapted_title + "\n\n" + section["content"]


def summarize_tasks(tasks_single_str):
    total = 0
    for task_str in tasks_single_str.split("\n"):
        result = re.search(r'Оценка\D*(\d+)ч.*', task_str)
        if result:
            hours_str = result.group(1)
            total += int(hours_str) if hours_str.isdigit() else 0
    return total

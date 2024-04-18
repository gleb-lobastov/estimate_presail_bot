def russian_plural(number, word_forms):
    """
    Склоняет слово в соответствии с переданным числом.

    Args:
        number (int): Число, для которого нужно выбрать правильную форму слова.
        word_forms (list): Список форм слова в порядке: [единственное число, для двух, для пяти].

    Returns:
        str: Склоненная форма слова.

    Example:
        russian_plural(5, ['яблоко', 'яблока', 'яблок']) вернет 'яблок'
    """
    remainder_100 = number % 100
    remainder_10 = number % 10

    if remainder_100 in [11, 12, 13, 14]:
        return word_forms[2]
    elif remainder_10 == 1:
        return word_forms[0]
    elif remainder_10 in [2, 3, 4]:
        return word_forms[1]
    else:
        return word_forms[2]
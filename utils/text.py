def find_nearest_split(text, max_length, max_seek_distance):
    length_to_stop_seek = len(text) - max_seek_distance

    if len(text) < max_length:
        return len(text)

    split_pos = text.rfind("\n", 0, max_length)
    if split_pos < length_to_stop_seek:
        split_pos = text.rfind(" ", 0, max_length)
    if split_pos < length_to_stop_seek:
        split_pos = max_length
    return split_pos

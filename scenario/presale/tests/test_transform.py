import unittest
from ..transform import semantic_split, prepare_for_clean_prompt, clean

data = {
    "md": (
            "# title 1\n" +
            "content 1...\n" +
            "############# whatever\n" +
            "whatever content\n"
            "# title 2\n" +
            "content 2.1...\n" +
            "content 2.2...\n" +
            "content 2.3..."
    ),
    "sections": [
        {"pos": 0, "title": "# title 1", "content": "content 1..."},
        {"pos": 23, "title": "############# whatever", "content": "whatever content"},
        {"pos": 63, "title": "# title 2", "content": "content 2.1...\ncontent 2.2...\ncontent 2.3..."},
    ],
    "clean_prompt": "# title 1//>0\n############# whatever//>23\n# title 2//>63",
    "clean_prompt_response": "1. title_1//>0\n2. title_2//>63",
    "clean_sections": [
        {"pos": 0, "title": "1. title_1", "content": "content 1..."},
        {"pos": 63, "title": "2. title_2", "content": "content 2.1...\ncontent 2.2...\ncontent 2.3..."},
    ],
}


class TestSections(unittest.TestCase):
    def test_split(self):
        sections = semantic_split(data["md"])
        self.assertEqual(
            sections,
            data["sections"],
            'The result of split_by_sectionsis wrong.'
        )

    def test_prepare_for_clean_prompt(self):
        self.assertEqual(
            prepare_for_clean_prompt(data["sections"]),
            data["clean_prompt"],
            'The result of prepare_sections_for_clean_prompt is wrong.'
        )

    def test_clean(self):
        self.assertEqual(
            clean(data["sections"], data["clean_prompt_response"]),
            data["clean_sections"],
            'The result of clean_sections is wrong.'
        )

    if __name__ == '__main__':
        unittest.main()

import unittest
from utils.telegram import split_to_chunks


class TestTelegramUtils(unittest.TestCase):
    def test_split_to_chunks_return_seek_max_dist(self):
        test_content = "123456789012345678901234567890\n1234567890"
        chunks = split_to_chunks(test_content, max_message_length=40, seek_distance_len=10)
        self.assertEqual(
            chunks,
            ["123456789012345678901234567890\n123456789", "0"],
            'The result of split_by_sectionsis wrong.'
        )

    def test_split_to_chunks_space_seek_max_dist(self):
        test_content = "123456789012345678901234567890 1234567890"
        chunks = split_to_chunks(test_content, max_message_length=40, seek_distance_len=10)
        self.assertEqual(
            chunks,
            ["123456789012345678901234567890 123456789", "0"],
            'The result of split_to_chunks is wrong.'
        )

    def test_split_to_chunks_return(self):
        test_content = "123456789012345678901234567890\n123456789"
        chunks = split_to_chunks(test_content, max_message_length=40, seek_distance_len=10)
        self.assertEqual(
            chunks,
            ["123456789012345678901234567890", "123456789"],
            'The result of split_to_chunks wrong.'
        )

    def test_split_to_chunks_space(self):
        test_content = "123456789012345678901234567890 123456789"
        chunks = split_to_chunks(test_content, max_message_length=40, seek_distance_len=10)
        self.assertEqual(
            chunks,
            ["123456789012345678901234567890", "123456789"],
            'The result of split_to_chunks wrong.'
        )

    def test_split_to_chunks_enough_len(self):
        test_content = "23456789012345678901234567890 1234567890"
        chunks = split_to_chunks(test_content, max_message_length=40, seek_distance_len=10)
        self.assertEqual(
            chunks,
            ["23456789012345678901234567890 1234567890"],
            'The result of split_to_chunks wrong.'
        )

    if __name__ == '__main__':
        unittest.main()

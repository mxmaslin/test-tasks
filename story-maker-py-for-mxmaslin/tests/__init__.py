import unittest

from main import TextFormatter


class TestTextFormatter(unittest.TestCase):
    @classmethod
    def setUp(cls):
        words = ["Elis", "no", "say", ",", "!", "but", "Burt", "din't", "herd", "her", ".", "maybe", "?", "not",
                 "{username}", "noise", "was", "here"]
        order = [0, 3, 1, [2, 18], [4, 21], 5, 6, 7, 8, 9, [10, 15], [11, 13], 12, 14, 16, 17, 19, 20]
        exclude = ["noise"]
        cls._formatter = TextFormatter(words, order, exclude)

    def test_get_as_list(self):
        elems = self._formatter.get_as_list("Egor")
        self.assertEqual(elems,
                         ["Elis", "say", ",", "no", "!", "but", "Burt", "din't", "herd", "her", ".", "maybe", "?",
                          "maybe", "not", ".", "Egor", ",", "was", "here", "!"])

    def test_get_as_text(self):
        txt = self._formatter.get_as_text("Egor")
        self.assertEqual(txt, "Elis say, no! But Burt din't herd her. Maybe? Maybe not. Egor, was here!")

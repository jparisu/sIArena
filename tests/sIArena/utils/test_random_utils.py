import unittest
from unittest.mock import patch

from sIArena.utils.random_utils import (
    random_consonant,
    random_pronounceable_name,
    random_vowel,
)


class TestRandomUtils(unittest.TestCase):
    def test_random_vowel_uses_vowel_pool(self):
        with patch("sIArena.utils.random_utils.random.choice", return_value="e") as choice_mock:
            value = random_vowel()

        self.assertEqual(value, "e")
        self.assertEqual(choice_mock.call_args.args[0], "aeiou")

    def test_random_consonant_uses_consonant_pool(self):
        with patch("sIArena.utils.random_utils.random.choice", return_value="z") as choice_mock:
            value = random_consonant()

        self.assertEqual(value, "z")
        self.assertEqual(choice_mock.call_args.args[0], "bcdfghjklmnpqrstvwxyz")

    def test_random_pronounceable_name_alternates_consonants_and_vowels(self):
        with patch("sIArena.utils.random_utils.random_consonant", side_effect=["b", "d", "f"]) as consonant_mock:
            with patch("sIArena.utils.random_utils.random_vowel", side_effect=["a", "e"]) as vowel_mock:
                name = random_pronounceable_name(5)

        self.assertEqual(name, "badef")
        self.assertEqual(consonant_mock.call_count, 3)
        self.assertEqual(vowel_mock.call_count, 2)

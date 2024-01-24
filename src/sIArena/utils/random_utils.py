import random
from typing import List


def random_vowel() -> str:
    """Returns a random vowel"""
    return random.choice("aeiou")

def random_consonant() -> str:
    """Returns a random consonant"""
    return random.choice("bcdfghjklmnpqrstvwxyz")

def random_pronounceable_name(length: int = 5) -> str:
    """Returns a random name of given length that intercaletes vowels and consonants"""
    return "".join([random_consonant() if i % 2 == 0 else random_vowel() for i in range(length)])

# -*-coding: utf-8 -*-

from __future__ import annotations

from random import randint, shuffle
import string

try:
    from secrets import choice
except ImportError:
    from random import choice


class PasswordGenerator:
    """Random password generator that follows the rules

    Args:
        length (int): Length of the password (one or two parameters)
            - One parameter:  fixed_length
            - Two parameters: minimum_length, maximum_length
        rules (dict[str, int]): Rules for password generation
            default:
                - It has lowercase at least one
                - It has uppercase at least one
                - It has digits at least one
                - It has symbol at least one
        uniques (int): Number of unique characters (default: 0)
    """

    def __init__(
            self, *length: int,
            rules: dict[str, int] = {
                string.ascii_lowercase: 1,
                string.ascii_uppercase: 1,
                string.digits: 1,
                string.punctuation: 1,
            },
            uniques: int = 0):
        if len(length) == 1 and length[0] > 0:
            max_length = length[0]
            min_length = length[0]
        elif len(length) == 2 and 0 < length[0] < length[1]:
            min_length, max_length = length
        else:
            raise ValueError("'length' is wrong")

        if not all(v >= 0 for v in rules.values()):
            raise ValueError("ruled_lengths must be over 0)")
        ruled_length = sum(rules.values())
        if ruled_length > min_length:
            raise ValueError("The ruled length exceeds the minimum length")
        self._min = min_length - ruled_length
        self._max = max_length - ruled_length
        self._rules = rules.copy()
        letters = ''.join(self._rules.keys())
        self._letters = ''.join(set(letters))

        if uniques == -1:
            self._uniques = max_length
        elif uniques <= max_length:
            self._uniques = uniques
        else:
            raise ValueError(
                "'uniques' must be between -1 and password length")
        max_uniques = len(self._letters)
        if not self._uniques <= max_uniques:
            raise ValueError(f"'uniques' must be less than {max_uniques}")

    def generate(self) -> str:
        """Generate a password according to rules

        Returns:
            str: Generated password
        """
        self._rules[self._letters] = randint(self._min, self._max)
        while True:
            choiced_chars = [
                choice(k)
                for k, v in self._rules.items()
                for i in range(v)
            ]
            unique_chars = set(choiced_chars)
            if (len(unique_chars) == len(choiced_chars)
                    or len(unique_chars) >= self._uniques):
                shuffle(choiced_chars)
                return ''.join(choiced_chars)

    def bulk_generate(self, count: int = 1, unique: bool = False) -> list[str]:
        """Generate passwords according to rules

        Args:
            count (int): Number of passwords
            unique (bool): Uniqueness of the password to be generated

        Returns:
            list[str]: Generated passwords
        """
        if unique:
            passwords = set()
            while len(passwords) < count:
                passwords.add(self.generate())
            return list(passwords)
        else:
            return [self.generate() for i in range(count)]

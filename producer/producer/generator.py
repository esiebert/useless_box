"""Module holding generator implementations used by the producer."""
# pylint: disable=too-few-public-methods
from random import choice
from string import ascii_letters, digits
from typing import Generator

CHARACTERS = ascii_letters + digits


def twenty_digits_code() -> Generator[str, None, None]:
    """Generates a 20 digits alphanumeric code."""
    while True:
        yield ''.join([choice(CHARACTERS) for _ in range(20)])

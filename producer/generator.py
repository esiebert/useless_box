"""Module holding generator implementations used by the producer."""
from abc import ABC, abstractmethod
from random import choice
from string import ascii_letters, digits

CHARACTERS = ascii_letters + digits


class Generator(ABC):
    """Abstract implementation of a Generator."""
    @abstractmethod
    def generate(self):
        """Abstract implementation of generation function."""

class TwentyDigitsCode(Generator):
    """Generator that generates 20 digits alphanumeric codes."""
    def generate(self):
        """Generates the alphanumeric code."""
        return ''.join([choice(CHARACTERS).upper() for _ in range(20)])

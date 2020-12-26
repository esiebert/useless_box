from abc import ABC, abstractmethod
from random import choice
from string import ascii_letters, digits


CHARACTERS = ascii_letters + digits


class Generator(ABC):
	@abstractmethod
	def generate():
		pass

class TwentyDigitsCode(Generator):
	def generate(self):
		return ''.join([choice(CHARACTERS).upper() for _ in range(20)])

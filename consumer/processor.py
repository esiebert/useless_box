"""Module holding implementation of processors."""
from abc import ABC, abstractmethod


class Processor(ABC):
    """Abstract implementation of a processor."""
    @abstractmethod
    def process(self, body):
        """Abstract function that processes the body."""

class SumNumbers(Processor):
    """Processor which sums all the numbers in a string."""
    def process(self, body):
        return sum([int(val) for val in str(body) if val.isnumeric()])

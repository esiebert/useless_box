"""Module holding implementations of output streams."""
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod


class OutputStream(ABC):
    """Abstract implementation of a output stream."""
    @abstractmethod
    def write(self, timestamp, body, result):
        """Abstract function that writes into the output stream."""

class FileOutputStream(OutputStream):
    """Output stream that writes to a given file."""
    def __init__(self, filepath):
        self._filepath = filepath

    def write(self, timestamp, body, result):
        """Saves measurements in a file."""
        with open(self._filepath, 'a') as file:
            file.write(f"{timestamp},{body},{result}\n")

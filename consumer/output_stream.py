from abc import ABC, abstractmethod


class OutputStream(ABC):
    @abstractmethod
    def write():
        pass

class FileOutputStream(OutputStream):
    def __init__(self, filepath):
        self._filepath = filepath

    def write(self, timestamp, body, result):
        """Saves measurements in a file."""
        with open(self._filepath, 'a') as f:
            f.write(f"{timestamp},{body},{result}\n")

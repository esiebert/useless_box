"""Module holding implementations of output streams."""
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod
from redis import Redis
import logging

LOGGER = logging.getLogger('consumer.output_stream')


class OutputStream(ABC):
    """Abstract implementation of a output stream."""
    @abstractmethod
    def write(self, timestamp: str, body: bytes, result: str) -> None:
        """Abstract function that writes into the output stream."""


class FileOutputStream(OutputStream):
    """Output stream that writes to a given file."""
    def __init__(self, filepath: str) -> None:
        self._filepath = filepath

    def write(self, timestamp: str, body: bytes, result: str) -> None:
        """Saves measurements in a file."""
        with open(self._filepath, 'a') as file:
            file.write(f"{timestamp},{str(body)},{result}\n")


class RedisOutputStream(OutputStream):
    """Output stream that writes to redis."""
    def __init__(self, host: str, port: int, db: int) -> None:
        try:
            self.r = Redis(host=host, port=port, db=db)
        except Exception as e:
            LOGGER.error("Unable to initialize Redis: %s", e)
            raise

    def write(self, timestamp: str, body: bytes, result: str) -> None:
        """Saves measurements in redis."""
        try:
            self.r.set(timestamp, f"{str(body)},{result}")
        except Exception as e:
            LOGGER.error("Unable to set value in Redis: %s", e)
            raise

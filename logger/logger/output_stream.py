"""Module holding implementations of output streams."""
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod
from redis import Redis
import logging
from serial import Serial

LOGGER = logging.getLogger('logger.output_stream')


class OutputStream(ABC):
    """Abstract implementation of a output stream."""
    @abstractmethod
    def write(self, timestamp: str, body: str, result: str) -> None:
        """Abstract function that writes into the output stream."""


class FileOutputStream(OutputStream):
    """Output stream that writes to a given file."""
    def __init__(self, filepath: str) -> None:
        self._filepath = filepath

    def write(self, timestamp: str, body: str, result: str) -> None:
        """Saves measurements in a file."""
        with open(self._filepath, 'a') as file:
            file.write(f"{timestamp},{body},{result}\n")


class RedisOutputStream(OutputStream):
    """Output stream that writes to redis."""
    def __init__(self, host: str, port: int, db: int) -> None:
        try:
            self.r = Redis(host=host, port=port, db=db)
        except Exception as e:
            LOGGER.error("Unable to initialize Redis: %s", e)
            raise

    def write(self, timestamp: str, body: str, result: str) -> None:
        """Saves measurements in redis."""
        try:
            self.r.set(timestamp, f"{body},{result}")
        except Exception as e:
            LOGGER.error("Unable to set value in Redis: %s", e)
            raise


class SerialOutputStream(OutputStream):
    """Output stream that writes to serial port."""
    def __init__(self, port: str, baudrate: int,) -> None:
        try:
            self._serial = Serial(port, baudrate)
        except Exception as e:
            LOGGER.error("Unable to initialize Serial: %s", e)
            raise

    def write(self, timestamp: str, body: str, result: str) -> None:
        """Write measurements to serial."""
        send_body = bytes("%s\r" % result, 'ascii')
        LOGGER.error("Sending %s", send_body)
        try:
            self._serial.write(send_body)
        except Exception as e:
            LOGGER.error("Unable to send value through serial: %s", e)
            raise

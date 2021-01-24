"""Module holding implementation of processors."""
import logging
from random import randint
from time import sleep

LOGGER = logging.getLogger('consumer.processor')


def sum_numbers(body: str) -> int:
    """Simulates processing time and sums all the numbers in a string."""
    LOGGER.error("Processing body...")
    sleep(randint(4, 8))
    return sum([int(val) for val in str(body) if val.isnumeric()])

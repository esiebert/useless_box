"""
The Meter component produces random values between 0 and 9000.00
and queues it in RabbitMQ.
"""
import logging
import random
import string
from time import sleep
from common.message_broker import RabbitMQ
import os

LOGGER = logging.getLogger('producer')
CHARACTERS = string.ascii_letters + string.digits

# Duration of interval between sends
INTERVAL_SEC = 5

class Producer():
    def __init__(self):
        self._message_broker = RabbitMQ(
            service='producer'
        )

    def start(self):
        """Main loop which queues random 20 digits alphanumerical strings."""
        LOGGER.error(f"Starting production!")
        while True:
            code = _generate_string()
            self._message_broker.publish(body=code)
            LOGGER.error(f"Sent {code}")
            sleep(INTERVAL_SEC)

def _generate_string():
    return ''.join([random.choice(CHARACTERS).upper() for _ in range(20)])

if __name__ == '__main__':
    producer = Producer()
    producer.start()

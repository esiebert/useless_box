"""
The Meter component produces random values between 0 and 9000.00
and queues it in RabbitMQ.
"""
import logging
import random
import string
from time import sleep
from common.rabbitmq import setup as setup_rabbitmq
import os

LOGGER = logging.getLogger('producer')
CHARACTERS = string.ascii_letters + string.digits

# Duration of interval between sends
INTERVAL_SEC = 5

class Producer():
    def __init__(self):
        self._channel = setup_rabbitmq(
            service='producer'
        )

    def start(self):
        """Main loop which queues random alphanumerical codes of length 20."""
        while True:
            code = _generate_string()
            self._channel.basic_publish(exchange='', routing_key=os.environ.get("RABBITMQ_QUEUE", "codes"), body=code)
            LOGGER.error(f"Sent {code}")
            sleep(INTERVAL_SEC)

def _generate_string():
    return ''.join([random.choice(CHARACTERS).upper() for _ in range(20)])

if __name__ == '__main__':
    producer = Producer()
    producer.start()

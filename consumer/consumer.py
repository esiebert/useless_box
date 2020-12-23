"""
The PV Simulator component consumes values queued by a meter in RabbitMQ
and sums up with estimated photovoltaic values at a give timestamp. The
summed up value is then saved in a log file.
"""
import logging
from time import sleep
from datetime import datetime
from common.rabbitmq import setup as setup_rabbitmq
import random

LOGGER = logging.getLogger('consumer')

# Log filepath
LOG_FILEPATH = "./log.txt"

class Consumer():
    def __init__(self):
        self._channel = setup_rabbitmq(
            callback_function=self.callback,
            service='producer'
        )

    def start(self):
        LOGGER.error("Consuming RabbitMQ queue.")
        self._channel.start_consuming()

    def log_value(self, timestamp, body, result):
        """Saves measurements and saves to a log file."""
        with open(LOG_FILEPATH, 'a') as f:
            f.write(f"{timestamp},{body},{result}\n")

    def process_value(self, body):
        """Procedure holding core functionality.

        Receives a string and sums all the numbers in it.
        """
        timestamp = datetime.utcnow()

        # Sum all the numbers in the string
        result = sum([int(val) for val in body if val.isnumeric()])

        # Log time, string, and result of sum
        LOGGER.error(f"Result is {result} for processed value {body}")
        self.log_value(timestamp, body, result)

    def callback(self, ch, method, properties, body):
        """Callback function to handle and process RabbitMQ messages."""
        self.process_value(str(body))

if __name__ == '__main__':
    consumer = Consumer()
    consumer.start()

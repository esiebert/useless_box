import logging
from time import sleep
from common.message_broker import MessageBroker, RabbitMQ
from generator import Generator, TwentyDigitsCode

LOGGER = logging.getLogger('producer')

# Duration of interval between sends
INTERVAL_SEC = 5

class Producer():
    def __init__(self, message_broker: MessageBroker, generator: Generator):
        self._message_broker = message_broker
        self._generator = generator

    def start(self):
        """Main loop which queues random 20 digits alphanumerical strings."""
        LOGGER.error(f"Starting production!")
        while True:
            body = self._generator.generate()
            self._message_broker.publish(body=body)
            LOGGER.error(f"Sent {body}")
            sleep(INTERVAL_SEC)

if __name__ == '__main__':
    producer = Producer(
        message_broker=RabbitMQ(
            service='producer'
        ),
        generator=TwentyDigitsCode(),
    )
    producer.start()

"""Module that implements the consumer."""
# pylint: disable=too-few-public-methods
import logging
from datetime import datetime
import json
from typing import Callable

from common.message_broker import MessageBroker, RabbitMQ
from consumer.processor import sum_numbers

LOGGER = logging.getLogger('consumer')

# Log filepath
LOG_FILEPATH = "./log.txt"


class Consumer():
    """
    Implementation of a consumer which processes messages queued in a message broker
    and sends it to logger.
    """
    def __init__(self,
            message_broker: MessageBroker,
            processor: Callable,
        ) -> None:
        self._processor = processor
        self._message_broker = message_broker
        message_broker.setup_callback(self._callback)

    def start(self) -> None:
        """Starts consuming queued messages from the message broker."""
        LOGGER.error("Starting consumption!")
        self._message_broker.start_consuming()

    # pylint: disable=[unused-argument, invalid-name]
    def _callback(self, ch, method, properties, body: bytes) -> None:
        """Callback function to handle and process messages."""
        str_body = body.decode('ascii')
        result = self._processor(str_body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        LOGGER.error("Result is %s for processed value %s", str(result), str_body)

        # Log time, string, and result of sum
        log_body = json.dumps({
            'timestamp': str(datetime.utcnow()),
            'code': str_body,
            'result': result,
        })
        self._message_broker.publish(body=log_body)

if __name__ == '__main__':
    consumer = Consumer(
        message_broker=RabbitMQ(
            service='consumer',
            consume_queue='codes',
            publish_queue='logs'
        ),
        processor=sum_numbers,
    )
    consumer.start()

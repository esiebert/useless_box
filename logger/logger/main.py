"""Module that implements the logger."""
# pylint: disable=too-few-public-methods
import logging
import json

from common.message_broker import MessageBroker, RabbitMQ
from logger.output_stream import OutputStream, SerialOutputStream

LOGGER = logging.getLogger('logger')

# Log filepath
LOG_FILEPATH = "./log.txt"


class Logger():
    """
    Implementation of a logger which receives messages queued in a message broker
    and logs the output.
    """
    def __init__(self,
            message_broker: MessageBroker,
            output_stream: OutputStream
        ) -> None:
        self._output_stream = output_stream
        self._message_broker = message_broker
        message_broker.setup_callback(self._callback)

    def start(self) -> None:
        """Starts consuming queued messages from the message broker."""
        LOGGER.error("Starting consumption!")
        self._message_broker.start_consuming()

    # pylint: disable=[unused-argument, invalid-name]
    def _callback(self, ch, method, properties, body: bytes) -> None:
        """Callback function to handle and log messages."""
        ch.basic_ack(delivery_tag=method.delivery_tag)
        LOGGER.error("Got logs %s", str(body))
        body_dict = json.loads(body)

        # Log time, string, and result of sum
        self._output_stream.write(
            body_dict['timestamp'],
            body_dict['code'],
            body_dict['result']
        )

if __name__ == '__main__':
    logger = Logger(
        message_broker=RabbitMQ(
            service='logger',
            consume_queue='logs',
        ),
        output_stream=SerialOutputStream(
            port='/dev/ttyACM1',
            baudrate=115200,
        ),
    )
    logger.start()

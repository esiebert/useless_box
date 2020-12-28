"""Module that implements the consumer."""
# pylint: disable=too-few-public-methods
import logging
from datetime import datetime
from output_stream import OutputStream, FileOutputStream
from processor import Processor, SumNumbers
from common.message_broker import MessageBroker, RabbitMQ

LOGGER = logging.getLogger('consumer')

# Log filepath
LOG_FILEPATH = "./log.txt"


class Consumer():
    """
    Implementation of a consumer which processes messages queued in a message broker
    and logs the output.
    """
    def __init__(self,
            message_broker: MessageBroker,
            processor: Processor,
            output_stream: OutputStream
        ):
        self._processor = processor
        self._output_stream = output_stream
        self._message_broker = message_broker
        message_broker.setup_callback(self._callback)

    def start(self):
        """Starts consuming queued messages from the message broker."""
        LOGGER.error("Starting consumption!")
        self._message_broker.start_consuming()

    # pylint: disable=[unused-argument, invalid-name]
    def _callback(self, ch, method, properties, body):
        """Callback function to handle and process messages."""
        result = self._processor.process(body)
        LOGGER.error("Result is %s for processed value %s", str(result), str(body))

        # Log time, string, and result of sum
        timestamp = datetime.utcnow()
        self._output_stream.write(timestamp, body, result)

if __name__ == '__main__':
    consumer = Consumer(
        message_broker=RabbitMQ(
            service='consumer'
        ),
        processor=SumNumbers(),
        output_stream=FileOutputStream(
            filepath=LOG_FILEPATH
        ),
    )
    consumer.start()

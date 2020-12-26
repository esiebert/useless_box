import pika
import logging
from time import sleep
import os

from abc import ABC, abstractmethod


class MessageBroker(ABC):
    """Abstract Message Broker class"""
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _setup(self):
        pass

    @abstractmethod
    def setup_callback(self):
        pass

    @abstractmethod
    def publish(self):
        pass

    @abstractmethod
    def start_consuming(self):
        pass


class RabbitMQ(MessageBroker):
    def __init__(self, service='rabbitmq'):
        self._host = os.environ.get("RABBITMQ_HOST", "localhost")
        self._port = os.environ.get("RABBITMQ_PORT", 5672)
        self._user = os.environ.get("RABBITMQ_USER", "guest")
        self._pwd = os.environ.get("RABBITMQ_PWD", "guest")
        self._queue = os.environ.get("RABBITMQ_QUEUE", "codes")
        self._logger = logging.getLogger(service)
        self._channel = self._setup(service)

    def _setup(self, service='rabbitmq'):
        """Sets up a channel to RabbitMQ Message Broker"""
        tries = 5
        while True:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self._host,
                        port=self._port,
                        credentials=pika.PlainCredentials(
                            self._user,
                            self._pwd
                        )
                    )
                )
                channel = connection.channel()
                channel.queue_declare(queue=self._queue)
                return channel
            except pika.exceptions.ProbableAuthenticationError as e:
                self._logger.error("Error while authenticating on RabbitMQ")
                raise e
            except pika.exceptions.AuthenticationError as e:
                self._logger.error("Error while authenticating on RabbitMQ")
                raise e
            except pika.exceptions.ConnectionClosedByBroker as e:
                self._logger.error("Connection was closed unexpectedly")
                raise e
            except Exception as e:
                tries -= 1
                if tries == 0:
                    self._logger.error(f"Unexpected error on RabbitMQ: {e}")
                    raise e
                self._logger.error("Waiting for RabbitMQ to start...")
                sleep(2)

    def setup_callback(self, callback_function):
        self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=callback_function,
            auto_ack=False
        )

    def publish(self, body):
        self._channel.basic_publish(
            exchange='',
            routing_key=self._queue,
            body=body
        )

    def start_consuming(self):
        self._channel.start_consuming()

"""Module holding implementation of message brokers."""
import logging
from time import sleep
import os
from abc import ABC, abstractmethod

import pika


class MessageBroker(ABC):
    """Abstract implementation of a message broker."""
    @abstractmethod
    def _setup(self):
        """Abstract function which sets up the message broker."""

    @abstractmethod
    def setup_callback(self, callback_function):
        """Abstract function which sets up the callback."""

    @abstractmethod
    def publish(self, body):
        """Abstract function which publish a body to the message broker."""

    @abstractmethod
    def start_consuming(self):
        """Abstract function which starts the consumption of messages queued."""


class RabbitMQ(MessageBroker):
    """Implementation of a message broker using RabbitMQ"""
    def __init__(self, service='rabbitmq'):
        self._host = os.environ.get("RABBITMQ_HOST", "localhost")
        self._port = os.environ.get("RABBITMQ_PORT", 5672)
        self._user = os.environ.get("RABBITMQ_USER", "guest")
        self._pwd = os.environ.get("RABBITMQ_PWD", "guest")
        self._queue = os.environ.get("RABBITMQ_QUEUE", "codes")
        self._logger = logging.getLogger(service)
        self._channel = self._setup()

    # pylint: disable=invalid-name
    def _setup(self):
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
            except Exception as e: # pylint: disable=broad-except
                tries -= 1
                if tries == 0:
                    self._logger.error("Unexpected error on RabbitMQ: %s", e)
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

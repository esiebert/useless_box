import pika
import logging
from time import sleep
import os

def setup(callback_function=None, service='rabbitmq'):
    """Sets up a channel to RabbitMQ Message Broker"""
    LOGGER = logging.getLogger(service)
    tries = 5
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=os.environ.get("RABBITMQ_HOST", ""),
                    port=os.environ.get("RABBITMQ_PORT", 0),
                    credentials=pika.PlainCredentials(
                        os.environ.get("RABBITMQ_USER", ""),
                        os.environ.get("RABBITMQ_PWD", "")
                    )
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue=os.environ.get("RABBITMQ_QUEUE", "codes"))
            if callback_function:
                channel.basic_consume(
                    queue=os.environ.get("RABBITMQ_QUEUE", "codes"), 
                    on_message_callback=callback_function, 
                    auto_ack=False
                )
            return channel
        except Exception as e:
            tries -= 1
            if tries == 0:
                LOGGER.error(f"Unable to connect to RabbitMQ: {e}")
                raise e
            LOGGER.error("Waiting for RabbitMQ to start...")
            sleep(2)
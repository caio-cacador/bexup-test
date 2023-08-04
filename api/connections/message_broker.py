import json
import pika
import os
import logging
from typing import List


LOGGER = logging.getLogger("uvicorn.error")
CAR_QUEUE_NAME=os.getenv('CAR_QUEUE_NAME')
TRUCK_QUEUE_NAME=os.getenv('TRUCK_QUEUE_NAME')
MOTORCYCLE_QUEUE_NAME=os.getenv('MOTORCYCLE_QUEUE_NAME')


class MessageBrokerConnection:
    """
    Create the RabbitMQ connection
    """

    def __init__(self):
        """
        Create the RabbitMQ connection and channel
        """
        self.__connection = pika.BlockingConnection(
            pika.URLParameters(os.getenv("MESSAGE_BROKER_URL"))
        )
        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(CAR_QUEUE_NAME)
        self.__channel.queue_declare(TRUCK_QUEUE_NAME)
        self.__channel.queue_declare(MOTORCYCLE_QUEUE_NAME)
        LOGGER.info(f"Message broker connected.")

    def publish_messages(self, messages: List[dict], queue: str):
        """
        Publish the message to RabbitMQ
        """
        try:
            for message in messages:
                self.__channel.basic_publish(
                    exchange="",
                    body=json.dumps(message),
                    routing_key=queue
                )
            LOGGER.info(f"{len(messages)} messages sent to queue {queue}.")
        except Exception as ex:
            LOGGER.error(f"An error has occurred in publish method: {ex}")
            
    def close_connection(self):
        if self.__channel.is_open:
            self.__channel.close()
        if self.__connection.is_open:
            self.__connection.close()
        LOGGER.info(f"Message broker disconnected.")
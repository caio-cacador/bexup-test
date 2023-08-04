import json
import pika
import os
import logging
from typing import List


LOGGER = logging.getLogger("uvicorn.error")


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
        self.__queue_name = os.getenv("MESSAGE_BROKER_CHARGER_CHANNEL")
        LOGGER.info(f"Message broker connected.")

    def publish_messages(self, messages: List[dict]):
        """
        Publish the message to RabbitMQ
        """
        try:
            for message in messages:
                self.__channel.basic_publish(
                    exchange="",
                    body=json.dumps(message),
                    routing_key=self.__queue_name
                )
            LOGGER.info(f"{len(messages)} messages sent.")
        except Exception as ex:
            LOGGER.error(f"An error has occurred in publish method: {ex}")
            
    def close_connection(self):
        if self.__channel.is_open:
            self.__channel.close()
        if self.__connection.is_open:
            self.__connection.close()
        LOGGER.info(f"Message broker disconnected.")
import logging
import time
import traceback
import pika
import os

from typing import Callable
from exceptions.message_broker import NackException, AckException


LOGGER = logging.getLogger("sLogger")
CONSUMER_RECONNECT_DELAY = 120


class MessageBrokerConsumerConnection:
    def __init__(self, channels: list):
        LOGGER.debug("Connecting to RabbitMQ ...")
        self.reconnect_delay = CONSUMER_RECONNECT_DELAY
        self.channels = channels
        self.start_connection()
        
    def start_connection(self):
        self.connection = pika.SelectConnection(
            parameters=pika.URLParameters(os.getenv("MESSAGE_BROKER_URL")),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )

    def on_connection_open(self, connection):
        LOGGER.debug("Connected to RabbitMQ, creating a new channel")
        connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        for channel_spec in self.channels:
            LOGGER.debug(f"Connected in {channel_spec.channel_name} channel")
            channel.queue_declare(channel_spec.channel_name)
            channel.basic_consume(channel_spec.channel_name, channel_spec.on_message)

    def on_connection_open_error(self, _unused_connection, err):
        LOGGER.critical(f"Failed to connect to RabbitMQ - {err}")
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        LOGGER.critical(f"RabbitMQ connection closed - {reason}")
        self.reconnect()

    def reconnect(self):
        LOGGER.debug(f"Attempting to reconnect in {self.reconnect_delay} seconds")
        time.sleep(self.reconnect_delay)
        self.start_connection()
        self.start()

    def start(self):
        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            LOGGER.error(traceback.format_exc())
            LOGGER.critical("KeyboardInterrupt error")
            self.connection.close()


class Queue:
    def __init__(self, channel_name: str, callback: Callable):
        self.channel_name = channel_name
        self.callback = callback

    def on_message(self, channel, method_frame, _header_frame, body) -> None:
        LOGGER.debug(f"The {self.channel_name} channel has a new message")
        message_body = body.decode("utf8")
        try:
            self.callback(message_body)
            LOGGER.debug("Work done!")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        except NackException:
            LOGGER.error(traceback.format_exc())
            LOGGER.critical("NackException - Resending Message to Queue")
            channel.basic_nack(delivery_tag=method_frame.delivery_tag)

        except AckException:
            LOGGER.error(traceback.format_exc())
            LOGGER.critical("AckException - Work done.")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        except Exception as error:
            LOGGER.error(traceback.format_exc())
            LOGGER.critical(f"Unknown Error - Resending Message to Queue: {error}")
            channel.basic_nack(delivery_tag=method_frame.delivery_tag)

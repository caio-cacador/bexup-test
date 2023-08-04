import os
from services.charger import ChargerService
from connections.message_broker import (
    Queue,
    MessageBrokerConsumerConnection
)
import logging


logging.getLogger("sLogger")

CAR_QUEUE_NAME=os.getenv('CAR_QUEUE_NAME')
TRUCK_QUEUE_NAME=os.getenv('TRUCK_QUEUE_NAME')
MOTORCYCLE_QUEUE_NAME=os.getenv('MOTORCYCLE_QUEUE_NAME')



def main():
    message_broken = MessageBrokerConsumerConnection(
        channels=[
            Queue(CAR_QUEUE_NAME, ChargerService().charge_car),
            Queue(TRUCK_QUEUE_NAME, ChargerService().charge_truck),
            Queue(MOTORCYCLE_QUEUE_NAME, ChargerService().charge_motorcycle),
        ]
    )
    message_broken.start()


if __name__ == "__main__":
    main()

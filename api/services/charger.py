import asyncio
import logging
from connections.vehicles import VehiclesConnection
from connections.message_broker import (
    MessageBrokerConnection,
    CAR_QUEUE_NAME,
    TRUCK_QUEUE_NAME,
    MOTORCYCLE_QUEUE_NAME
)


LOGGER = logging.getLogger("uvicorn.error")


class ChargerService():
    def __init__(self) -> None:
        self.vehicles_connection = VehiclesConnection()
        self.message_broker_con = MessageBrokerConnection()

    async def __charge_car_brands(self):
        car_brands = await self.vehicles_connection.get_all_car_brands()
        LOGGER.info(f"Found {len(car_brands)} car brands.")
        self.message_broker_con.publish_messages(car_brands, CAR_QUEUE_NAME)
        LOGGER.info(f"Car brands sent.")

    async def __charge_truck_brands(self):
        truck_brands = await self.vehicles_connection.get_all_truck_brands()
        LOGGER.info(f"Found {len(truck_brands)} truck brands.")
        self.message_broker_con.publish_messages(truck_brands, TRUCK_QUEUE_NAME)
        LOGGER.info(f"Truck brands sent.")

    async def __charge_motorcycle_brands(self):
        motorcycle_brands = await self.vehicles_connection.get_all_motorcycle_brands()
        LOGGER.info(f"Found {len(motorcycle_brands)} motorcycle brands.")
        self.message_broker_con.publish_messages(motorcycle_brands, MOTORCYCLE_QUEUE_NAME)
        LOGGER.info(f"Motorcycle brands sent.")

    async def execute_initial_charge(self):
        coros = [
            self.__charge_car_brands(),
            self.__charge_motorcycle_brands(),
            self.__charge_truck_brands()
        ]
        await asyncio.gather(*coros, return_exceptions=True)
        self.message_broker_con.close_connection()

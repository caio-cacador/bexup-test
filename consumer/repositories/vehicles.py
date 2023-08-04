import os
from pymongo import MongoClient
import logging


LOGGER = logging.getLogger("sLogger")


class VehiclesRepository():
    def __init__(self) -> None:
        client = MongoClient(os.getenv('MONGO_DB_URL'))
        database = client[os.getenv('MONGO_DB_DATABASE')]
        self._collection = database[os.getenv('MONGO_DB_COLLECTION')]
        
    def save(
        self,
        vehicle_type: str,
        brand_code: str,
        brand_name: str,
        models: str,
        years: str
    ):
        try:
            result = self._collection.replace_one(
                filter=dict(vehicle_type=vehicle_type, brand_code=brand_code),
                replacement=dict(
                    vehicle_type=vehicle_type,
                    brand_code=brand_code,
                    brand_name=brand_name,
                    models=models,
                    years=years
                ),
                upsert=True
            )
            upserted_id = str(result.upserted_id)
            
            LOGGER.info(f"Vehicle {upserted_id} updated")
            return upserted_id
        except Exception as ex:
            LOGGER.critical(f"Error during the vehicle update: {ex}")
            raise Exception

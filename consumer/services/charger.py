import json
from repositories.vehicles import VehiclesRepository
from connections.vehicles import VehiclesConnection


class ChargerService():
    def __init__(self) -> None:
        self.vehicles_repo = VehiclesRepository()
        self.vehicles_con = VehiclesConnection()
        
    def unpack_message(self, message_body: str):
        """
        Arguments:
            message_body (str): Message properties
        """
        message_body = json.loads(message_body)
        return message_body['codigo'], message_body['nome']
    
    def charge_car(self, message_body: str):
        """
        Arguments:
            message_body {str} -- Message properties

        Raises:
            AckException: raise if message processing is completed
            Exception: raise if some unknown error happen
        """
        brand_code, brand_name = self.unpack_message(message_body)
        result = self.vehicles_con.get_car_models_by_brand(brand_code)
        self.vehicles_repo.save(
            vehicle_type='car',
            brand_code=brand_code,
            brand_name=brand_name,
            models=result.get('modelos', []),
            years=result.get('anos', [])
        )
        
    def charge_truck(self, message_body: str):
        """
        Arguments:
            message_body {str} -- Message properties

        Raises:
            AckException: raise if message processing is completed
            Exception: raise if some unknown error happen
        """
        brand_code, brand_name = self.unpack_message(message_body)
        result = self.vehicles_con.get_truck_models_by_brand(brand_code)
        self.vehicles_repo.save(
            vehicle_type='truck',
            brand_code=brand_code,
            brand_name=brand_name,
            models=result.get('modelos', []),
            years=result.get('anos', [])
        )

    def charge_motorcycle(self, message_body: str):
        """
        Arguments:
            message_body {str} -- Message properties

        Raises:
            AckException: raise if message processing is completed
            Exception: raise if some unknown error happen
        """
        brand_code, brand_name = self.unpack_message(message_body)
        result = self.vehicles_con.get_motorcycle_models_by_brand(brand_code)
        self.vehicles_repo.save(
            vehicle_type='motorcycle',
            brand_code=brand_code,
            brand_name=brand_name,
            models=result.get('modelos', []),
            years=result.get('anos', [])
        )

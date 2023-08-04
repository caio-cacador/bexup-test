import requests
from http import HTTPStatus
from typing import List
from exceptions.vehicles_connection import ServiceUnavailableError


class VehiclesConnection:
    
    def __init__(self) -> None:
        self.__base_url = "https://parallelum.com.br/fipe/api/v1"
    
    @property
    def __headers(self):
        return {"Content-Type": "application/json"}
    
    def _get(self, vehicle: str, brand: str) -> List[dict]:
        response  = requests.get(
            f"{self.__base_url}/{vehicle}/marcas/{brand}/modelos",
            headers=self.__headers
        )

        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            raise ServiceUnavailableError()

    def get_car_models_by_brand(self, brand) -> List[dict]:
        return self._get(vehicle="carros", brand=brand)

    def get_truck_models_by_brand(self, brand) -> List[dict]:
        return self._get(vehicle="caminhoes", brand=brand)

    def get_motorcycle_models_by_brand(self, brand) -> List[dict]:
        return self._get(vehicle="motos", brand=brand)

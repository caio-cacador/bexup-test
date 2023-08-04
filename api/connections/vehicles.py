import httpx
from http import HTTPStatus
from typing import List
from api.exceptions.base import ServiceUnavailableError


class VehiclesConnection:
    
    def __init__(self) -> None:
        self.__base_url = "https://parallelum.com.br/fipe/api/v1"
    
    @property
    def __headers(self):
        return {"Content-Type": "application/json"}
    
    async def __get(self, url_sulfix: str) -> List[dict]:
        async with httpx.AsyncClient() as client:
            response  = await client.get(
                f"{self.__base_url}{url_sulfix}",
                headers=self.__headers
            )

        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            raise ServiceUnavailableError()

    async def get_all_car_brands(self) -> List[dict]:
        return await self.__get("/carros/marcas")

    async def get_all_truck_brands(self) -> List[dict]:
        return await self.__get("/caminhoes/marcas")

    async def get_all_motorcycle_brands(self) -> List[dict]:
        return await self.__get("/motos/marcas")

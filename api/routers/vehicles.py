from typing import List
from fastapi import APIRouter
from http import HTTPStatus
from api.services.charger import ChargerService


router = APIRouter(prefix='/vehicles', tags=['Vehicles'])


@router.post("/initial_charge")
async def initial_charge():
    """
    Execute the initial charge on database
    """
    await ChargerService().execute_initial_charge()

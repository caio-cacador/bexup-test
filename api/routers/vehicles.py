from typing import List
from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from http import HTTPStatus
from services.charger import ChargerService
from services.vehicles import VehiclesService
from exceptions.base import NotFoundError
from models.vehicles import (
    VehiclesBrandsResponseModel,
    VehiclesInfoResponseModel,
    VehiclesUpdateModel,
    VehiclesUpdateResponseModel
)



RESPONSE_404 = {404: {"description": "Not found"}}
RESPONSE_503 = {503: {"description": "Service Unavailable"}}

router = APIRouter(prefix='/vehicles', tags=['Vehicles'])


@router.post("/initial_charge", responses=RESPONSE_503)
async def initial_charge():
    """
    Execute the initial charge in database
    """
    await ChargerService().execute_initial_charge()


@router.get(
    "/brands",
    response_description="List all brand in database",
    response_model=List[VehiclesBrandsResponseModel]
)
async def get_all_brands():
    """
    Get all brands in database
    """
    return await VehiclesService().get_all_brands()


@router.get(
    "/brands/{brand}",
    responses=RESPONSE_404,
    response_description="List all data in database with filtered brand",
    response_model=List[VehiclesInfoResponseModel]
)
async def get_details(brand: str = Path(examples=['Acura', 'Cadillac', 'Dodge'])):
    """
    Get all brands in database by query
    
    Args: brand : str

    """
    try:
        return await VehiclesService().get_models_by_brand_name(brand)
    except NotFoundError:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"message": f"Brand '{brand}' not found."}
        )


@router.get(
    "/brands/{brand}",
    responses=RESPONSE_404,
    response_description="List all data in database with filtered brand",
    response_model=List[VehiclesInfoResponseModel]
)
async def get_details(brand: str = Path(examples=['Acura', 'Cadillac', 'Dodge'])):
    """
    Get all brands in database by query
    
    Args: brand : str

    """
    try:
        return await VehiclesService().get_models_by_brand_name(brand)
    except NotFoundError:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"message": f"Brand '{brand}' not found."}
        )


@router.post(
    "/brands",
    responses=RESPONSE_404,
    response_description="Update a brand in database",
    response_model=VehiclesUpdateResponseModel
)
async def post_details(brand: VehiclesUpdateModel):
    """
    Update a brand in database
    
    Args: brand : ObjectId - MongoDB ID

    """
    try:
        return await VehiclesService().update(brand)
    except NotFoundError:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"message": f"Brand ID '{brand.id}' not found."}
        )

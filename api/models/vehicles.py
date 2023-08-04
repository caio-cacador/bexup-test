from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic import BaseModel


class VehiclesBrandsResponseModel(BaseModel):
    id: str = Field(alias="_id")
    code: str = Field(..., alias="brand_code")
    name: str = Field(..., alias="brand_name")


class VehiclesModel(BaseModel):
    code: int = Field(..., alias="codigo")
    name: str = Field(..., alias="nome")


class VehiclesInfoResponseModel(BaseModel):
    id: str = Field(alias="_id")
    vehicle_type: str
    code: str = Field(..., alias="brand_code")
    observation: Optional[str] = Field(default="")
    models: List[VehiclesModel]


class VehiclesUpdateModel(BaseModel):
    id: str
    vehicle_type: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    observation: Optional[str] = None
    models: Optional[List[VehiclesModel]] = None


class VehiclesYearsResponseModel(BaseModel):
    code: str = Field(..., alias="codigo")
    name: str = Field(..., alias="nome")


class VehiclesModelUpdateResponseModel(BaseModel):
    code: int = Field(..., alias="code")
    name: str = Field(..., alias="name")


class VehiclesUpdateResponseModel(BaseModel):
    id: str = Field(alias="_id")
    vehicle_type: str
    code: str = Field(..., alias="brand_code")
    name: str = Field(..., alias="brand_name")
    observation: Optional[str] = Field(default="")
    models: List[VehiclesModelUpdateResponseModel]
    years: List[VehiclesYearsResponseModel]

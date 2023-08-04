from repositories.vehicles import VehiclesRepository
from models.vehicles import VehiclesUpdateModel


class VehiclesService():
    def __init__(self) -> None:
        self.vehicles_repo = VehiclesRepository()
        
    def _remove_object_id(self, items):
        if isinstance(items, dict):
            items['_id'] = str(items['_id'])
        elif isinstance(items, list):
            return [self._remove_object_id(i) for i in items]
        return items

    async def get_all_brands(self):
        res = await self.vehicles_repo.get_all_brands()
        return self._remove_object_id(res)
    
    async def get_models_by_brand_name(self, brand: str):
       res = await self.vehicles_repo.get_by_brand_name(brand)
       return self._remove_object_id(res)
    
    async def update(self, brand: VehiclesUpdateModel):
        res = await self.vehicles_repo.update(**brand.dict())
        return self._remove_object_id(res)

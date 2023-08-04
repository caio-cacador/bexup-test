import os
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import ReturnDocument
from exceptions.base import NotFoundError
from bson import ObjectId


class VehiclesRepository():
    def __init__(self) -> None:
        client = AsyncIOMotorClient(os.getenv('MONGO_DB_URL'))
        database = client[os.getenv('MONGO_DB_DATABASE')]
        self.collection = database[os.getenv('MONGO_DB_COLLECTION')]
        
    async def get_all_brands(self) -> List[dict]:
        cursor = self.collection.find(
            {},
            {'brand_code': 1, 'brand_name': 1}
        )
        documents = [document async for document in cursor]

        if documents:
            return documents
        raise NotFoundError()

    async def get_by_brand_name(self, brand_name) -> List[dict]:
        cursor = self.collection.find(
            {'brand_name': brand_name}, 
            {'years': 0, 'brand_name': 0}
        )
        documents = [document async for document in cursor]

        if documents:
            return documents
        raise NotFoundError()

    async def update(self, **kargs) -> dict:
        _id = kargs.pop('id')
        data = {k:v for k, v in kargs.items() if v is not None}
        
        doc_updated = await self.collection.find_one_and_update(
            {'_id': ObjectId(_id)}, 
            {'$set': data},
            return_document=ReturnDocument.AFTER
        )

        if doc_updated is None:
            raise NotFoundError()
        return doc_updated

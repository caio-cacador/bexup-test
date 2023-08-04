from pymongo.mongo_client import MongoClient


class MongoConnection:
    client: MongoClient = None


db = MongoConnection()


def get_client():
    return db.client

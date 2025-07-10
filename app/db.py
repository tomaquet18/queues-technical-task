import motor.motor_asyncio
from functools import lru_cache

@lru_cache
def get_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongodb:27017")
    return client["domain_scanner"]
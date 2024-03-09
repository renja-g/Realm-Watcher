from app.core import config
from app import models

from motor.motor_asyncio import AsyncIOMotorClient

from beanie import init_beanie


async def init_db() -> None:
    client = AsyncIOMotorClient(config.settings.DEFAULT_MONGODB_URI)
    db = client[config.settings.DEFAULT_DATABASE_DB]
    await init_beanie(database=db, document_models=models.__all_models__)   

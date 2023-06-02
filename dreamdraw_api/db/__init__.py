
import motor.motor_asyncio
from dreamdraw_api import config

client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB_URL)
db = client[config.MONGODB_NAME]


async def get_database():
    return db
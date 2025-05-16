# import aioredis
import redis
from src.config import Config

TOKEN_EXPIRY = 3600

redis_block_list = redis.asyncio.Redis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0
)


async def add_jwt_id_to_block_list(jid:str):
    await redis_block_list.set(
        name=jid, value=jid, ex=TOKEN_EXPIRY
    )


async def is_added_to_block_list(jid:str):
    # if not found in the list -- this will output None
    res = await redis_block_list.get(name=jid) 
    return res is not None


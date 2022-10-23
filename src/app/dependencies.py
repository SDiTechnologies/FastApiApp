from os import environ
from fastapi import Header, HTTPException
import aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis_om import get_redis_connection

# safe location for storing credentials without creating circular imports
# from app.models.Constants import REDIS_DATA_URL, REDIS_CACHE_URL
from app.data.constants import REDIS_DATA_URL, REDIS_CACHE_URL, SMTP_CREDENTIALS

### NO, NO, NO!!! Stop trying to make circular dependencies work!!
# from app.models.Emails import SmtpHandler, Email
database = get_redis_connection(url=REDIS_DATA_URL, decode_responses=True)
# r = aioredis.from_url(REDIS_CACHE_URL, encoding='utf8', decode_responses=True)
# FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")


####################################################
## SECTION: Http Headers
####################################################
async def get_token_header(x_token: str = Header()):
    if x_token != "fake-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")

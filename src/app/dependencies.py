from os import environ
from fastapi import Header, HTTPException
import aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis_om import get_redis_connection


REDIS_DATA_URL = environ.get("REDIS_OM_URL")
REDIS_CACHE_URL = (
    environ.get("REDIS_CACHE_URL")
    if environ.get("REDIS_CACHE_URL") is not None
    else REDIS_DATA_URL
)

database = get_redis_connection(url=REDIS_DATA_URL, decode_responses=True)
# r = aioredis.from_url(REDIS_CACHE_URL, encoding='utf8', decode_responses=True)
# FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")

SMTP_CREDENTIALS = {
    "host": environ.get("SMTP_HOST"),
    "port": environ.get("SMTP_PORT"),
    "username": environ.get("SMTP_USERNAME"),
    "password": environ.get("SMTP_PASSWORD"),
    "tls": environ.get("SMTP_TLS"),
    "ssl": environ.get("SMTP_SSL"),
}


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")

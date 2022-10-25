from fastapi import Depends, FastAPI
import aioredis
from app.dependencies import get_query_token, get_token_header
from app.internal import admin
from app.routers import items, sessions, speedtests, users, customers, emails

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# from redis_om import get_redis_connection
from redis_om import Migrator

from app.dependencies import REDIS_DATA_URL, REDIS_CACHE_URL
from app.data import seeder


app = FastAPI(
    # dependencies=[Depends(get_query_token)]
)


# sample routes
app.include_router(users.router)
app.include_router(items.router)
app.include_router(customers.router)

# utility routes
app.include_router(sessions.router)
app.include_router(speedtests.router)
app.include_router(emails.router)

# admin routes; TODO: (go-thru)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.on_event("startup")
async def startup():
    print(
        f"launching with configuration values:\n[DATA] {REDIS_DATA_URL}\n[CACHE] {REDIS_CACHE_URL}"
    )
    r = aioredis.from_url(REDIS_CACHE_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")

    # create data indices if not exist
    # Migrator().run()

    # seed data =)
    # seeder.seed_data()

    # # You can set the Redis OM URL using the REDIS_OM_URL environment
    # # variable, or by manually creating the connection using your model's
    # # Meta object.
    # Customer.Meta.database = get_redis_connection(url=REDIS_DATA_URL, decode_responses=True)

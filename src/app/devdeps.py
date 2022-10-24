from json import dumps, loads
from requests import Session

import asyncio
import aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis_om import Migrator, get_redis_connection

from app.dependencies import REDIS_CACHE_URL, REDIS_DATA_URL, SMTP_CREDENTIALS

from app.models.Customers import FakeCustomer, Customer
from app.models.Recipes import FakeRecipe, Recipe


from app.models.Emails import Email, SmtpHandler, FakeEmail

# # from app.models.Accounts import Account, AccountTransaction, FakeAccount
# from app.models.Accounts import (
#     Address,
#     OwnerDetail,
#     Owner,
#     Account,
#     AccountTransaction,
#     FakeAccount,
# )


url = "http://localhost:8000/"

headers = {
    # user agent
    "User-Agent": "Narwhal Sarcophagus Fluffy Walrus; (v0.0.1a)",
    # accepts, encoding, etc...
    "Content-Type": "application/json",
    # 'Accept': 'application/json'
}

sess = Session()
sess.headers = headers

# configure redis connections
r = aioredis.from_url(REDIS_CACHE_URL, encoding="utf8", decode_responses=True)
FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")


c = FakeCustomer()
c.join_date = c.join_date.strftime("%Y-%m-%d")

e = FakeEmail()

smtpHandler = SmtpHandler.from_dict(SMTP_CREDENTIALS)

# create indices for terminal python session
Migrator().run()


# def run_async(func):
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.gather(func))
#     loop.close()

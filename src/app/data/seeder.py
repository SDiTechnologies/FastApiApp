from typing import Any
import random
from app.models.Customers import FakeCustomer
from app.models.Emails import FakeEmail
from app.models.Recipes import FakeRecipe
from app.models.Accounts import FakeAccountTransaction, FakeAccount


# data seeder exists to avoid the mundane task of having to recreate these objects manually each time the volume is destroyed
# fortunately, since the fake classes inherit from the Redis-OM JsonModel, all of the object methods for querying are available to the fakers as well which deems it unnecessary to import the base objects
def seed_data():
    objs = [FakeEmail]
    # objs = [FakeCustomer, FakeEmail, FakeRecipe, FakeAccount]
    # # TODO: create derived sets, transactions, and similarly related objects (simulate RDBMS using Redis)
    # derived_objs = [FakeAccountTransaction]
    try:
        [create_set(obj) for obj in objs]
    except Exception as e:
        print(f"{e}")


def create_set(obj: Any):
    if not set_exists(obj):
        n = random.randint(5, 15)
        print(f"Creating {n} new object group sets: {str(obj)}")
        try:
            [obj().save() for i in range(n)]
        except Exception as e:
            print(f"{e}")


# def create_derived_set(obj: Any, *args):
#     if not set_exists(obj):
#         roll = (random.randint(1, 100)/100)
#         n = roll * 100
#         try:
#             for arg in args:


def set_exists(obj) -> bool:
    return bool(obj().find().all())

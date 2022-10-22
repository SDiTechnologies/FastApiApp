from typing import Any
import random
from app.models.Customers import FakeCustomer
from app.models.Emails import FakeEmail
from app.models.Recipes import FakeRecipe
from app.models.Accounts import FakeAccount


# data seeder exists to avoid the mundane task of having to recreate these objects manually each time the volume is destroyed
# fortunately, since the fake classes inherit from the Redis-OM JsonModel, all of the object methods for querying are available to the fakers as well which deems it unnecessary to import the base objects
def seed_data():
    objs = [FakeCustomer, FakeEmail, FakeRecipe, FakeAccount]
    try:
        [create_set(obj) for obj in objs]
    except Exception as e:
        print(f"{e}")


def create_set(obj: Any):
    if not bool(obj().find().all()):
        n = random.randint(5, 15)
        try:
            [obj().save() for i in range(n)]
        except Exception as e:
            print(f"{e}")

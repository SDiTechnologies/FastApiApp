import datetime
from typing import Optional
from redis_om import HashModel, Field
from pydantic import EmailStr

import factory

from app.models.common import BaseModel


class Customer(BaseModel):
    first_name: str
    last_name: str = Field(index=True)
    email: EmailStr
    join_date: datetime.date = Field(index=True)
    age: int = Field(index=True)
    bio: Optional[str]


class FakeCustomer(factory.Factory):
    class Meta:
        model = Customer

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    # email = factory.Faker('email')
    email = factory.LazyAttribute(
        lambda obj: "%s.%s@%s"
        % (obj.first_name.lower(), obj.last_name.lower(), "example.com")
    )
    join_date = factory.Faker("date")
    age = factory.Faker("random_int", min=13, max=30)
    bio = factory.Faker("paragraph", nb_sentences=4)

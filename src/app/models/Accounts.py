import datetime
import random
from dateutil.relativedelta import relativedelta

from redis_om import Field

import factory

from app.models.common import BaseModel, DerivedModel


# TODO: Review and restructure models as necessary
class Address(DerivedModel):
    ln1: str
    ln2: str | None
    city: str = Field(index=True)
    state: str = Field(index=True)
    postal_code: str = Field(index=True)


class OwnerDetail(DerivedModel):
    dob: datetime.date = Field(index=True)
    kba: str
    weight: float
    height: float


# seperated for confidentiality (leaner models + less hashing, encryption/decryption == less computing resources required)
class Owner(DerivedModel):
    fname: str = Field(index=True)
    lname: str = Field(index=True)
    owner_detail: OwnerDetail = Field(index=True)
    address: Address = Field(index=True)


class Account(BaseModel):
    number: str = Field(index=True)
    balance: float = Field(index=True)
    created: datetime.date = Field(index=True)
    accessed: datetime.date = Field(index=True)
    modified: datetime.date = Field(index=True)
    owner: Owner = Field(index=True)


class AccountTransaction(BaseModel):
    payor_id: str = Field(index=True)
    # payor: Account
    payee_id: str = Field(index=True)
    # payee: Account
    amount: float = Field(index=True)
    created: datetime.date = Field(index=True)
    posted: datetime.date = Field(index=True)


### Fakers
class FakeAddress(factory.Factory):
    class Meta:
        model = Address

    ln1 = factory.Faker("street_address")
    ln2 = factory.Faker("building_number")
    city = factory.Faker("city")
    state = factory.Faker(
        "random_element",
        elements=(
            "AZ",
            "CA",
            "NY",
            "IL",
            "OH",
            "NM",
            "ND",
            "FL",
            "LA",
            "AK",
            "AR",
            "MO",
            "TX",
            "CO",
        ),
    )
    postal_code = factory.Faker("postcode")


class FakeOwnerDetail(factory.Factory):
    class Meta:
        model = OwnerDetail

    dob = factory.Faker(
        "date_between_dates",
        date_start=(datetime.datetime.now() - relativedelta(years=65)),
        date_end=datetime.datetime.now(),
    )
    kba = factory.Faker(
        "random_element",
        elements=(
            "first grade teacher?",
            "mother's maiden name?",
            "best friend in school?",
            "favorite subject?",
            "favorite colour?",
            "passphrase?",
        ),
    )
    weight = random.uniform(110.0, 225.0)
    height = random.uniform(52.0, 72.5)


class FakeOwner(factory.Factory):
    class Meta:
        model = Owner

    fname = factory.Faker("first_name")
    lname = factory.Faker("last_name")
    owner_detail = FakeOwnerDetail()
    # # TODO: restructure for accepting multiple accounts and account types, ie. 'savings', 'checking', 'mortgage', 'loan', etc...
    # account = FakeAccount()
    address = FakeAddress()


class FakeAccount(factory.Factory):
    class Meta:
        model = Account

    number = factory.Faker("aba")
    balance = random.uniform(25.00, 10000.00)
    created = factory.Faker(
        "date_between_dates",
        date_start=(datetime.datetime.now() - relativedelta(years=20)),
        date_end=datetime.datetime.now(),
    )
    accessed = factory.Faker(
        "date_between_dates",
        date_start=(datetime.datetime.now() - relativedelta(days=65)),
    )
    modified = factory.Faker(
        "date_between_dates",
        date_start=(datetime.datetime.now() - relativedelta(days=25)),
    )
    owner = FakeOwner()


# # TODO: these should be declared once accounts exist, NOT simultaneously
# class AccountTransaction(BaseModel):
#     # payor_id: str
#     payor: Account
#     # payee_id: str
#     payee: Account
#     amount: float = Field(index=True)
#     created: datetime.date = Field(index=True)
#     posted: datetime.date = Field(index=True)

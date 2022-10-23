from redis_om import Field
import factory
from app.models.common import DerivedModel


class Address(DerivedModel):
    ln1: str
    ln2: str | None
    city: str = Field(index=True)
    state: str = Field(index=True)
    postal_code: str = Field(index=True)


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

from typing import Optional, Any
from redis_om import Field, EmbeddedJsonModel

# from redis_om import HashModel, Field
# from redis_om import EmbeddedJsonModel, Field
from pydantic import AnyUrl

from random import randint

import factory

from app.models.common import BaseModel, DerivedModel


class Ingredient(DerivedModel):
    name: str = Field(index=True)
    unit: str = Field(index=True)  # should be float or other calculable type
    measurement: str = Field(index=True)


# class Author(DerivedModel):
#     name: str = Field(index=True)
#     url: Optional[AnyUrl] = Field(index=True)


class Recipe(BaseModel):
    title: str = Field(index=True)
    instructions: str = Field(index=True)
    # url: Optional[AnyUrl]
    ingredients: list[Ingredient]
    author: str = Field(index=True)
    # source_url: Optional[AnyUrl]


class FakeIngredient(factory.Factory):
    class Meta:
        model = Ingredient

    name = factory.Faker(
        "random_element",
        elements=(
            "cumin",
            "paprika",
            "salt",
            "ground black pepper",
            "freshly ground black pepper",
            "basil",
            "thyme",
            "oregano",
            "sage",
            "rosemary",
            "ground beef",
            "chicken",
            "pork loin",
            "parsley",
            "garlic",
            "onion",
            "tomato",
            "potato",
            "carrots",
            "pumpkin",
            "cinnamon",
        ),
    )
    unit = factory.Faker(
        "random_element",
        elements=("1/16", "1/8", "1/4", "1/3", "1/2", "2/3", "1/3", "1", "1 1/2", "2"),
    )
    measurement = factory.Faker(
        "random_element", elements=("Cup(s)", "Tbsp(s)", "tsp(s)", "lb(s)", "unit(s)")
    )


# class FakeAuthor(factory.Factory):
#     class Meta:
#         model = Author
#     name = factory.Faker('name')
#     # url = factory.Lazy
#     # url = factory.Faker('domain_name')
#     url = factory.LazyAttribute(lambda obj: 'http://%s.com' % (obj.name.replace(' ', '-')))


class FakeRecipe(factory.Factory):
    class Meta:
        model = Recipe

    # title = factory.LazyAttribute(lambda obj: 'Secret Recipe ')
    title = factory.Faker("bothify", text="Mystery Recipe ???-???-#####")
    instructions = factory.Faker("paragraph", nb_sentences=15)
    # url = factory.Faker('')
    # ingredients = factory.RelatedFactoryList(FakeIngredient, size=lambda: randint(3,7))
    ingredients = FakeIngredient.create_batch(size=randint(3, 7))
    author = factory.Faker("name")
    # author = FakeAuthor()

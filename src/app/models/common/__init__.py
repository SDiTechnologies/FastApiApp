from redis_om import HashModel, JsonModel, EmbeddedJsonModel, Field, Migrator
from app.dependencies import database


class BaseModel(JsonModel):
    class Meta:
        database = database


class DerivedModel(EmbeddedJsonModel):
    pass
    # class Meta:
    #     database = database


# class BaseModel(HashModel):
#     class Meta:
#         database = database

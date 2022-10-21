import datetime
from dateutil.relativedelta import relativedelta

from typing import Optional

from redis_om import Field

from random import randint
import factory

from app.models.common import BaseModel


# TODO: review and correct FakeEmail generator
class Email(BaseModel):
    sender: str = Field(index=True)
    recipients: Optional[list[str]] = Field(index=True)
    content_type: str = Field(index=True)
    subject: str
    message: str
    sent: int = Field(index=True)
    sent_at: datetime.date | None = Field(index=True)
    viewed: int = Field(index=True)
    viewed_at: datetime.date | None = Field(index=True)


# Faker generator
class FakeEmail(factory.Factory):
    class Meta:
        model = Email

    sender = factory.Faker("ascii_free_email")
    # recipients = [fake.ascii_free_email() for x in range(randint(1,5))]
    content_type = factory.Faker(
        "random_element", elements=("text/plain", "text/html", "multipart/alternative")
    )
    subject = factory.Faker("paragraph", nb_sentences=1)
    message = factory.Faker("paragraph", nb_sentences=randint(2, 7))
    # TODO: fix faker
    # none of the randomization works as intended... go figure ¯\_(ツ)_/¯
    sent = 1 if ((randint(0, 80) / 100) > 0.2) else 0
    sent_at = (
        factory.Faker(
            "date_between_dates",
            date_start=(datetime.datetime.now() - relativedelta(years=2)),
            date_end=datetime.datetime.now(),
        )
        if (sent == 1)
        else None
    )
    viewed = 1 if (((randint(0, 60) / 100) > 0.2) & (sent == 1)) else 0
    viewed_at = (
        factory.Faker(
            "date_between_dates", date_start=(sent_at), date_end=datetime.datetime.now()
        )
        if (viewed == 1)
        else None
    )

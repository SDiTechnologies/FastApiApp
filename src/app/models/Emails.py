import datetime
from dateutil.relativedelta import relativedelta

from typing import Optional, Any
from dataclasses import dataclass

# from aiosmtplib import SMTP as asyncSMTP
import aiosmtplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from redis_om import Field

from random import randint
import factory

from app.models.common import BaseModel

from traceback import print_exc


# TODO: review and correct FakeEmail generator
class Email(BaseModel):
    from_addr: str = Field(index=True)
    to_addr: Optional[list[str]] = Field(index=True)
    to_cc: Optional[list[str]] = Field(index=True)
    to_bcc: Optional[list[str]] = Field(index=True)
    content_type: str = Field(index=True)
    subject: str
    message: str
    # sent: int = Field(index=True)
    # sent_at: datetime.date | None = Field(index=True)
    # viewed: int = Field(index=True)
    # viewed_at: datetime.date | None = Field(index=True)


@dataclass
class SmtpHandler:
    host: str
    port: str  # changes based on the values of environment and tls/ssl (465, 25, etc... (may vary by provider))
    username: str
    password: str
    tls: bool = False
    ssl: bool = False

    @staticmethod
    def from_dict(obj: Any) -> "SmtpHandler":
        _host = str(obj.get("host"))
        _port = int(obj.get("port"))
        _username = (
            str(obj.get("username")) if obj.get("username") is not None else None
        )
        _password = (
            str(obj.get("password")) if obj.get("password") is not None else None
        )
        _tls = bool(obj.get("tls"))
        _ssl = bool(obj.get("ssl"))

        return SmtpHandler(_host, _port, _username, _password, _tls, _ssl)

    def send(self, email: Email) -> bool:
        result = False
        try:
            if email:
                # prepare message
                msg = MIMEMultipart()
                msg.preamble = email.subject
                msg["Subject"] = email.subject
                msg["From"] = email.from_addr
                msg["To"] = ", ".join(email.to_addr)
                if len(email.to_cc):
                    msg["Cc"] = ", ".join(email.to_cc)
                if len(email.to_bcc):
                    msg["Bcc"] = ", ".join(email.to_bcc)

                msg.attach(MIMEText(email.message, email.content_type, "utf-8"))

                # contact smtp server
                with smtplib.SMTP(host=self.host, port=self.port) as conn:
                    conn.set_debuglevel(True)
                    print(f"{self.username} {type(self.password)}")
                    if self.username:
                        try:
                            conn.login(self.username, self.password)
                        except Exception as e:
                            print(
                                f"Unable to login with provided credentials: {e} {print_exc()}"
                            )
                    try:
                        conn.send_message(msg)
                        result = True
                        # conn.sendmail(email.from_addr, email.to_addr, msg.as_string())
                        # conn.send_message(msg, msg['From'], msg['To'])
                    except Exception as e:
                        print(f"{e}: {print_exc()}")

                # # TODO: mark email as sent and proceed...
            else:
                raise Exception("Email Object Not Provided")
        except Exception as e:
            print(f"{e} {print_exc()}")
        finally:
            return result

    # async def send(self, email: Email):
    #     result = False
    #     try:
    #         print(f"Entering Asynchronous send method")
    #         print(f"current object: {self.__dict__}")
    #         if email:
    #             # prepare message
    #             msg = MIMEMultipart()
    #             msg.preamble = email.subject
    #             msg["Subject"] = email.subject
    #             msg["From"] = email.from_addr
    #             msg["To"] = ", ".join(email.to_addr)
    #             if len(email.to_cc):
    #                 msg["Cc"] = ", ".join(email.to_cc)
    #             if len(email.to_bcc):
    #                 msg["Bcc"] = ", ".join(email.to_bcc)

    #             msg.attach(MIMEText(email.message, email.content_type, "utf-8"))

    #             # contact smtp server
    #             # potential redundant declaration self.ssl, self.tls
    #             # potential error in asyncSMTP instantiation
    #             smtp = aiosmtplib.SMTP(
    #                 hostname=self.host, port=self.port, use_tls=self.ssl
    #             )

    #             # if self.tls:
    #             #     await smtp.starttls()
    #             # if bool(self.username):
    #             #     await smtp.login(self.username, self.password)
    #             await smtp.send_message(msg)
    #             result = True
    #             await smtp.quit()

    #             # TODO: mark email as sent and proceed...
    #         else:
    #             raise Exception("No Email Object Provided")
    #     except Exception as e:
    #         print(f"{e} {print_exc()}")
    #     finally:
    #         return result


# class FakeEmailRecipients(factory.Factory):
# recipents = factory.Faker('ascii_free_email')


# Faker generator
class FakeEmail(factory.Factory):
    class Meta:
        model = Email

    # from_addr = factory.Faker("ascii_free_email")
    from_addr = "sender@example.com"
    to_addr = ["receiver@example.com"]
    to_cc = []
    to_bcc = []
    # recipients = [fake.ascii_free_email() for x in range(randint(1,5))]
    content_type = factory.Faker(
        "random_element", elements=("text/plain", "text/html", "multipart/alternative")
    )
    subject = factory.Faker("paragraph", nb_sentences=1)
    message = factory.Faker("paragraph", nb_sentences=randint(2, 7))
    # TODO: fix faker
    # none of the randomization works as intended... go figure ¯\_(ツ)_/¯

    # sent = 1 if ((randint(0, 80) / 100) > 0.2) else 0
    # sent_at = (
    #     factory.Faker(
    #         "date_between_dates",
    #         date_start=(datetime.datetime.now() - relativedelta(years=2)),
    #         date_end=datetime.datetime.now(),
    #     )
    #     if (sent == 1)
    #     else None
    # )
    # viewed = 1 if (((randint(0, 60) / 100) > 0.2) & (sent == 1)) else 0
    # viewed_at = (
    #     factory.Faker(
    #         "date_between_dates", date_start=(sent_at), date_end=datetime.datetime.now()
    #     )
    #     if (viewed == 1)
    #     else None
    # )

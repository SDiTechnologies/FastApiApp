import datetime
from typing import Any
from redis_om import Field
from dataclasses import dataclass
import factory

from app.models.common import BaseModel, DerivedModel


class RequestDetail(DerivedModel):
    host: str = Field(index=True)
    accept_encoding: str = Field(index=True)
    user_agent: str = Field(index=True)
    # returning null?
    content_type: str | None = Field(index=True)
    query_string: str | None = Field(index=True)
    http_method: str = Field(index=True)
    performed: datetime.datetime = Field(index=True)

    def from_dict(obj: Any) -> "RequestDetail":
        _host = obj.get("host")
        _accept_encoding = obj.get("accept-encoding")
        # _accept = str(obj.get('accept'))
        # _connection = str(obj.get('connection'))
        _user_agent = obj.get("user-agent")
        _content_type = obj.get("content-type")
        _query_string = obj.get("query-string")
        _http_method = obj.get("http-method")
        _performed = datetime.datetime.now()
        return RequestDetail(
            host=_host,
            accept_encoding=_accept_encoding,
            user_agent=_user_agent,
            content_type=_content_type,
            query_string=_query_string,
            http_method=_http_method,
            performed=_performed,
        )


class ClientDevice(BaseModel):
    client_ip: str = Field(index=True)
    # client_port: int
    request_detail: RequestDetail = Field(index=True)

    def from_dict(obj: Any) -> "ClientDevice":
        _client_ip = obj.get("client-ip")
        # _client_port = int(obj.get('client-port'))
        _request_detail = RequestDetail.from_dict(obj.get("request-detail"))
        return ClientDevice(client_ip=_client_ip, request_detail=_request_detail)


##############################################################################
## Fakers
##############################################################################

# TODO: review attribute return values
class FakeRequestDetail(factory.Factory):
    class Meta:
        model = RequestDetail

    host = factory.Faker("domain_name")
    accept_encoding = factory.Faker("random_element", elements=["json", "text", "etc"])
    user_agent = factory.Faker("user_agent")
    content_type = factory.Faker(
        "random_element",
        elements=["application/json", "application/html", "application/text"],
    )
    query_string = None
    # query_string = factory.Faker('')
    http_method = factory.Faker(
        "random_element", elements=["GET", "PUT", "POST", "PATCH", "DELETE"]
    )


class FakeClientDevice(factory.Factory):
    class Meta:
        model = ClientDevice

    client_ip = "192.168.0.23"
    request_detail = factory.LazyAttribute(lambda x: FakeRequestDetail())
    # client_ip = factory.Faker('')

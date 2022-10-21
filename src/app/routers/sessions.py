from fastapi import APIRouter, Header

# from fastapi import Request

from starlette.requests import Request
from starlette.responses import Response

from json import dumps

from pprint import pprint

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
    # responses={404:}
)

# TODO: consider expanding to include other information: Server response headers and client submission headers; ip address; geolocation; provider?
@router.get("/")
async def read_sessions(
    request: Request, response: Response, user_agent: str | None = Header(default=None)
):
    client_ip = request.client.host
    client_port = request.client.port
    request_headers = {k: v for k, v in request.headers.items()}

    # print(f"{request.query_string}")
    # pprint(f"{request.__dict__}")
    # pprint(f"{request.scope.get('query_string')}")
    # print(f"{request.method}")
    # print(f"{dir(response)}")
    # print(f"{response.__dict__}")
    return {
        "client-ip": client_ip,
        "client-port": client_port,
        "http-method": request.method,
        "query-string": request.scope.get("query_string"),
        "headers": request_headers,
    }

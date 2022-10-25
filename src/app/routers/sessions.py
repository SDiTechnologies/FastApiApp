from fastapi import APIRouter, Header, BackgroundTasks

# import asyncio
# import ast

from json import loads

# from fastapi import Request  # this 'MAY' refer to the same object as starlette.requests

from starlette.requests import Request
from starlette.responses import Response

from app.models.Sessions import ClientDevice, RequestDetail


router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
    # responses={404:}
)

# TODO: consider expanding to include other information: Server response headers and client submission headers; ip address; geolocation; provider?

# use the root url to list session options; multiple decorators to increase options for endpoint
@router.get("/")
@router.put("/")
@router.post("/")
@router.patch("/")
@router.delete("/")
async def read_session(
    request: Request, response: Response, user_agent: str | None = Header(default=None)
):
    request_dict = {k: v for k, v in request.headers.items()}
    additional_detail = {
        "http-method": request.method,
        "query-string": request.scope.get("query_string"),
    }

    request_dict.update(additional_detail)

    obj_dict = {"client-ip": request.client.host, "request-detail": request_dict}

    try:
        # request_detail = RequestDetail.from_dict(obj_dict.get('request-detail'))
        # print(f"{request_detail}")

        client_device = ClientDevice.from_dict(obj_dict)
        # print(f"{client_device}")

        client_device.save()

        return {"client-device": client_device}

        # # print(f"{client_device_dict}")
        # # c = (client_device_dict)
        # # c = ClientDevice.from_dict(client_device_dict)
        # # print(f"{c}")
        # # print(f"{c.__dict__}")
        # # c.save()
        # client_device.save()
        # return {'client-device': client_device}
        # return {}
    except Exception as e:
        print(f"{e}")
        return {"message": f"{e}"}

    # # print(f"{type(c)} {c.__dict__}")
    # # print(f"{q}")
    # return {
    #     # "request": request_detail,
    #     # "additional": additional_detail,
    #     "client-device": c.__dict__
    # }

    # request_headers = {k: v for k, v in request.headers.items()}

    # # print(f"{request.query_string}")
    # # print(f"{request.__dict__}")
    # # print(f"{request.scope.get('query_string')}")
    # # print(f"{request.method}")
    # # print(f"{dir(response)}")
    # # print(f"{response.__dict__}")
    # return {
    #     "client": client_device_dict,
    #     "http-method": request.method,
    #     "query-string": request.scope.get("query_string"),
    #     "headers": request_headers,
    # }


@router.post("/")
async def save_session(client_device: ClientDevice):
    return client_device.save()


@router.get("/all")
async def read_sessions(request: Request):
    return {"sessions": ClientDevice.find().all()}

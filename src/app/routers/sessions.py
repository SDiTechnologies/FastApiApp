from fastapi import APIRouter, Header, BackgroundTasks
import asyncio
import ast

from json import loads

# from fastapi import Request

from starlette.requests import Request
from starlette.responses import Response

from app.models.Sessions import ClientDevice, RequestDetail

from app.models.Speedtests import SpeedtestResult

# not sure if this naming convention lacks clarity; for now all dataclass dumps that haven't been properly integrated will be found in the Classes module
from app.models.Classes import SpeedtestResponse

from traceback import print_exc

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
    # responses={404:}
)


async def perform_speedtest(log=True):
    try:
        # ## debug instance A - normal shell command
        # proc = await asyncio.create_subprocess_exec('ls', '-sahl', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        # stdout, stderr = await proc.communicate()

        # print(f"type: {type(stdout)} value: {stdout}")

        # decoded = stdout.decode('utf-8')
        # print(f"{decoded}")

        ## debug instance B - dict return shell command

        # # command requires speedtest ookla cli tool installed on running machine
        proc = await asyncio.create_subprocess_shell(
            "speedtest -p no -f json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()
        # print(f"stdout: {stdout}\nstderr: {stderr}")

        # some of the following operations may be unnecessary now that it uses json data
        decoded_data = stdout.decode("utf-8")
        json_data = loads(decoded_data)
        # response_dict = ast.literal_eval(decoded_data)
        # print(f"{repr(response_dict)}")
        # print(f"{json_data}")

        speedtest = SpeedtestResponse.from_dict(json_data)
        results_dict = speedtest.to_dict()
        results = SpeedtestResult.from_dict(results_dict)

        results.save()

    except Exception as e:
        print(f"{e} {print_exc()}")


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

    # # this works, but there's gotta be a better way to instantiate...
    # request_detail = RequestDetail(host=obj_dict.get('host'), accept_encoding=obj_dict.get('accept-encoding'), user_agent=obj_dict.get('user-agent'), content_type=obj_dict.get('content-type'), query_string=obj_dict.get('query-string'), http_method=obj_dict.get('http-method'))

    # client_device = ClientDevice(client_ip=client_dict.get('client-ip'), request_detail=request_detail)

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


##############################################################################
## Speedtest
##############################################################################
@router.get("/speedtest")
async def get_speedtest(background_tasks: BackgroundTasks):
    background_tasks.add_task(perform_speedtest)
    return {"message": "begin perform_speedtest"}

    # # proc = await asyncio.create_subprocess_exec('ls', '-sahl', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    # proc = await asyncio.create_subprocess_shell('speedtest -p no -f json', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    # stdout, stderr = await proc.communicate()

    # return {'values': {'stdout': stdout, 'stderr': stderr}}


# stdout: b'{"type":"result","timestamp":"2022-10-24T22:10:52Z","ping":{"jitter":0.649,"latency":8.272,"low":7.814,"high":9.027},"download":{"bandwidth":29702582,"bytes":207652963,"elapsed":7006,"latency":{"iqm":25.528,"low":13.488,"high":30.966,"jitter":2.319}},"upload":{"bandwidth":1329170,"bytes":15720936,"elapsed":11215,"latency":{"iqm":89.243,"low":3.653,"high":155.824,"jitter":24.453}},"packetLoss":0,"isp":"Cox Communications","interface":{"internalIp":"192.168.0.9","name":"eno1","macAddr":"EC:8E:B5:45:08:BE","isVpn":false,"externalIp":"98.161.213.187"},"server":{"id":16613,"host":"speedtest.rd.ph.cox.net","port":8080,"name":"Cox - Phoenix","location":"Phoenix, AZ","country":"United States","ip":"184.182.243.169"},"result":{"id":"95e17207-af79-43a0-b37b-82376cbf4870","url":"https://www.speedtest.net/result/c/95e17207-af79-43a0-b37b-82376cbf4870","persisted":true}}\n'
# stderr: b''

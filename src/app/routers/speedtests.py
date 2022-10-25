import asyncio
from fastapi import APIRouter, BackgroundTasks
from json import loads

from starlette.requests import Request
from starlette.responses import Response

from traceback import print_exc

from app.models.Classes import SpeedtestResponse
from app.models.Speedtests import SpeedtestResult


router = APIRouter(prefix="/speedtests", tags=["speedtests"])


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
        _data = loads(decoded_data)
        # response_dict = ast.literal_eval(decoded_data)
        # print(f"{repr(response_dict)}")
        # print(f"{json_data}")

        response = SpeedtestResponse.from_dict(_data)
        results_dict = response.to_dict()
        result = SpeedtestResult.from_dict(results_dict)

        result.save()

    except Exception as e:
        print(f"{e} {print_exc()}")


@router.get("/")
async def get_speedtest(background_tasks: BackgroundTasks):
    background_tasks.add_task(perform_speedtest)
    return {"message": "initiating speedtest"}


@router.get("/all")
async def get_speedtests(request: Request, response: Response):
    return {"speedtests": SpeedtestResult.find().all()}

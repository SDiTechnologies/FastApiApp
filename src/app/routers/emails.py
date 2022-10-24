from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache.decorator import cache

from redis_om import NotFoundError

from traceback import print_exc

# from app.dependencies import smtpHandler
from app.dependencies import SMTP_CREDENTIALS
from app.models.Emails import Email, SmtpHandler


router = APIRouter(
    prefix="/emails",
    tags=["emails"],
)


def send_smtp_message(email: Email, log=True):
    # create handler
    smtpHandler = SmtpHandler.from_dict(SMTP_CREDENTIALS)
    try:
        smtpHandler.send(email)
    except Exception as e:
        print(f"{e} {print_exc()}")

    # DEBUG code
    if log:
        with open("logs.txt", mode="a") as email_file:
            content = f"{email.__dict__}"
            email_file.write(content)


@router.post("/new")
async def save_email(email: Email):
    return email.save()


@router.get("/")
async def get_emails(request: Request, response: Response):
    return {"emails": Email.find().all()}


@router.get("/{pk}")
@cache(expire=10)
async def get_email(pk: str, request: Request, response: Response):
    try:
        return Email.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Email not found")


# replace entire entry
@router.put("/{pk}")
async def put_email(pk: str, email: Email, request: Request, response: Response):
    try:
        e = Email.get(pk)
        print(f"{e.__dict__} : {email.__dict__}")
        e.update(email)
    except Exception as e:
        print(f"{e}")


# replace subset of entry fields
@router.patch("/{pk}")
async def patch_email(pk: str, email: Email, request: Request, response: Response):
    pass


# try sending an email by url; we're not going to arbitrarily allow this feature directly though
@router.post("/{pk}")
async def send_email(
    pk: str, background_tasks: BackgroundTasks, request: Request, response: Response
):
    # TODO: multiple try clauses for more sophisticated error handling; try get pk -> NotFoundError, try sending email -> whatever error (timeout, connectionrefused, etc...)
    try:
        e = Email.get(pk)
        background_tasks.add_task(send_smtp_message, e)
        # update the email status here!!!
        # TODO: migrate to use RabbitMQ?
        return {"message": "Email sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Oh No it's bad!\n\n{e}")


# presume that we want to actually delete entries for now, but prepare a secondary method that modifies visibility
@router.delete("/{pk}")
async def delete_email(pk: str, request: Request, response: Response):
    try:
        Email.delete(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Email not found")


# @router.patch("/{pk}/update")

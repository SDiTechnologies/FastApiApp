from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache.decorator import cache

from redis_om import NotFoundError

from app.models.Emails import Email

router = APIRouter(
    prefix="/emails",
    tags=["emails"],
)


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


# presume that we want to actually delete entries for now, but prepare a secondary method that modifies visibility
@router.delete("/{pk}")
async def delete_email(pk: str, request: Request, response: Response):
    try:
        Email.delete(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Email not found")


# @router.patch("/{pk}/update")

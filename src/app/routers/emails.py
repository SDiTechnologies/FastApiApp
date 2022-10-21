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

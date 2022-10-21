from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response

# fastapi_cache removed; allow Redis to manage cache similar to memcache
from fastapi_cache.decorator import cache

from redis_om import NotFoundError

from app.models.Customers import Customer

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.post("/new")
async def save_customer(customer: Customer):
    return customer.save()


@router.get("/")
async def get_customers(request: Request, response: Response):
    # return {"customers": Customer.all_pks()}
    return {"customers": Customer.find().all()}


@router.get("/{pk}")
@cache(expire=10)
async def get_customer(pk: str, request: Request, response: Response):
    try:
        return Customer.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Customer not found")

from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache.decorator import cache

from redis_om import NotFoundError

from app.models.Accounts import Account, Owner, OwnerDetail, Address

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

# Step 1: introduce simple get queries for each imported object


# create here or in sections? sections will still need put/patch methods;
# also, how handle deletes? (delete and/or update value)
@router.post("/new")
async def save_account(account: Account):
    return account.save()


@router.get("/")
async def get_accounts(request: Request, response: Response):
    # return {"accounts": Account.all_pks()}
    return {"accounts": Account.find().all()}


@router.get("/{pk}")
@cache()
async def get_account(pk: str, request: Request, response: Response):
    try:
        return Account.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Account not found")


#############################################################


@router.get("/owners")
async def get_owners(request: Request, response: Response):
    # return {"accounts": Account.all_pks()}
    return {"owners": Owner.find().all()}


@router.get("/owners/{pk}")
@cache()
async def get_owner(pk: str, request: Request, response: Response):
    try:
        return Owner.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Owner not found")


#############################################################


# @router.get('/owner-detail/{pk}')
# async def get_owner_detail(pk: str, request: Request, response: Response):
#     # return {"accounts": Account.all_pks()}
#     # return {"accounts": Account.find().all()}
#     try:
#         o = Owner.get(pk)
#         print
#     # return {"owner_detail": Owner.}

# @router.get('/{pk}')
# @cache()
# async def get_account(pk: str, request: Request, response: Response):
#     try:
#         return Account.get(pk)
#     except NotFoundError:
#         raise HTTPException(status_code=404, detail="Account not found")


#############################################################


# @router.get('/owner-details')
# async def get_owner_details(request: Request, response: Response):
#     # return {"accounts": Account.all_pks()}
#     return {"accounts": Account.find().all()}

# @router.get('/{pk}')
# @cache()
# async def get_account(pk: str, request: Request, response: Response):
#     try:
#         return Account.get(pk)
#     except NotFoundError:
#         raise HTTPException(status_code=404, detail="Account not found")

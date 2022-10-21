# FastApiApp

An exploration of rapid development using FastAPI + Redis + uvicorn + Docker + docker compose.

<!-- https://pypi.org/project/fastapi/
https://www.datacamp.com/tutorial/introduction-fastapi-tutorial
https://www.c-sharpcorner.com/article/getting-started-with-fastapi/

https://fastapi.tiangolo.com/tutorial/bigger-applications/
https://fastapi.tiangolo.com/tutorial/header-params/
https://httpie.io/docs/cli/empty-headers-and-header-un-setting


https://redis.io/docs/manual/eviction/
https://redis.io/docs/manual/config/
https://fastapi.tiangolo.com/tutorial/bigger-applications/ -->


<!-- Informal collection of process notes for later reference when extending anticipated features -->

### Gotchas and Brief Process Overview Summarization


1. When running anything relative to the contained python module 'app' the default object naming conventions used by redis_om may conflict with those used by the API routes unless ran from the directory above app/, aka src/. The Pipfile will still be housed within the app/ directory to avoid overcluttering, but this may require address and similarly there is a duplicated requirements.txt in the projects workspace for use in building docker containers. DRY!

2. When using module faker and hashmodel together with the API the date field requires conversion to a string date value before converting to json for data submission.

```python
#!/usr/bin/env python3
from json import dumps
from requests import Session
from app.models.Customers import FakeCustomer

url = "localhost:8000/customers/new"

# configure request headers for session
headers = {"User-Agent": "Developer Automation; v0.0.1a"}

sess = Session()
sess.headers = headers

# create a fake customer
fakeCustomer = FakeCustomer()

# store by accessing the redis instance directly
fakeCustomer.save()

# when accessing the external fast api 'app' module
# convert date -> str
fakeCustomer.join_date = fakeCustomer.join_date.strftime('%Y-%m-%d')

# try posting the data as json string
with sess.post(url, data=dumps(fakeCustomer.__dict__) as resp:
    try:
        if resp.ok:
            print(f"{resp.content}")
        else:
            print(f"http status code response received: {resp.status_code}: {resp.reason}")
    except Exception as e:
        print(f"Exception: {e}")
```


3. A very quick, concise, and somewhat lacking overview of process:

```python
# Step 1: create object instance and relevant data fakers
# file: app/models/Emails.py
# ...
# BaseModel inherits from redis_om JsonModel with a database connection instantiated in app.dependencies
class Email(BaseModel):
    sender: str = 'sender@example.com'
    recipients: list[str] | None = ['receiver@example.com']
    content_type: str = 'text/html'
    subject: str
    message: str
    sent: bool
    sent_at: datetime.date
    viewed: bool
    viewed_at: datetime.date
# ... declare any fakers as needed; See models/Emails.py for more

# Step 2: create routers for the API to consume
# file: app/routers/emails.py

# ...
# import the relevant models
from app.models.Emails import Email

# declare a default router path and any necessary dependencies (auth, headers, etc...)
router = APIRouter(
    prefix="/emails",
    tags=["emails"],
)

# declare http access methods
@router.post('/new')
async def save_email(email: Email):
    return email.save()

@router.get('/')
async def get_emails(request: Request, response: Response):
    return {"emails": Email.find().all()}
# ...

# Step 3: add the object router to the root application instance
# file: app/main.py

# ...
from fastapi import FastAPI
from app.dependencies import get_token_header
from app.internal import admin
from app.routers import users, items, sessions, customers, emails

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(sessions.router)
app.include_router(customers.router)
app.include_router(emails.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
# ...

# Step 4: (optional) add the Model and corresponding Faker to the devdeps file and make some noise!!! (generate fake data)
# file: app/devdeps.py

from app.models.Emails import Email, FakeEmail

some_arbitrary_random_int = random.randint(20, 100)

for _ in range(some_arbitrary_random_int):
    FakeEmail().save()


# or to use the api endpoint instead
from requests import Session
from json import dumps

# our desired object api endpoint
url = r'http://localhost:8000/emails/new'
timefmt = '%Y-%m-%d'

# create requests session
sess = Session()

# update session headers and other attributes
sess.headers = {'User-Agent': 'Narwhal Sarcophagus Fluffy Walrus; (v0.0.0a)'}


# create a loop to submit session data to the API url endpoint
for _ in range(some_arbitrary_random_int):
    fakeEmail = FakeEmail()

    # TODO: fix; but for now the ever-present 'temporary' workaround (there's so much more wrong with this)
    # gotta convert datetime -> string for json to be received properly
    if (fakeEmail.sent_at):
        fakeEmail.sent_at = fakeEmail.sent_at.strftime(timefmt)
    if (fakeEmail.viewed_at):
        fakeEmail.viewed_at = fakeEmail.viewed_at.strftime(timefmt)

    with sess.post(url, data=dumps(fakeEmail.__dict__)) as resp:
        try:
            if resp.ok:
                print(f"Posted Object: {fakeEmail.__dict__}")
            else:
                print(f"Unsuccessful attempt to post object: {resp.reason}\nContent: {resp.content}")
        except Exception as e:
            print(f"Exception: {e}")
            pass
```

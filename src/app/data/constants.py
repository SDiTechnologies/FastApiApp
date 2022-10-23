from os import environ

####################################################
## SECTION: Redis
####################################################
REDIS_DATA_URL = environ.get("REDIS_OM_URL")
REDIS_CACHE_URL = (
    environ.get("REDIS_CACHE_URL")
    if environ.get("REDIS_CACHE_URL") is not None
    else REDIS_DATA_URL
)


####################################################
## SECTION: SMTP (aka email)
####################################################

SMTP_CREDENTIALS = {
    "host": environ.get("SMTP_HOST"),
    "port": environ.get("SMTP_PORT"),
    "username": environ.get("SMTP_USERNAME", None),
    "password": environ.get("SMTP_PASSWORD", None),
    "tls": environ.get("SMTP_TLS"),
    "ssl": environ.get("SMTP_SSL"),
}

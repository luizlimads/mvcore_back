from decouple import config

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS").split(",")

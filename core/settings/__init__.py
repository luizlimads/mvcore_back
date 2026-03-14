from decouple import config

ENV = config("DJANGO_ENV", default="local")

if ENV == "production":
    from .production import *
elif ENV == "homologation":
    from .homologation import *
else:
    from .local import *

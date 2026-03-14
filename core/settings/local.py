from .base import *
from .apps import *
from .middleware import *
from .database import *
from .auth import *
from .rest import *
from .cors import *
from .spectacular import *
from .email import *
from .celery import *

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

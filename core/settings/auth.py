from datetime import timedelta

AUTH_USER_MODEL = 'usuario.Usuario'

AUTHENTICATION_BACKENDS = [
    'usuario.authentication.EmailBackend',
]

AUTH_PASSWORD_VALIDATORS = []

DJOSER = {
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': "newpassword?id={uid}&token={token}",
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=600),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
}

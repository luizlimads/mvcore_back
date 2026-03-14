from celery.schedules import crontab
from decouple import config

CELERY_BROKER_URL = config(
    "CELERY_BROKER_URL",
    default="redis://127.0.0.1:6379/0"
)

CELERY_RESULT_BACKEND = config(
    "CELERY_RESULT_BACKEND",
    default=CELERY_BROKER_URL
)

CELERY_TIMEZONE = 'America/Sao_Paulo'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {

    # 'integracao-frequente': {
    #     'task': 'integrador.tasks.dispatcher_frequente.sincronizar_frequente',
    #     'schedule': crontab(minute=0),
    # },

    'integracao-diaria': {
        'task': 'integrador.tasks.dispatcher_diario.sincronizar_diario',
        'schedule': crontab(hour=1, minute=0),
    },

    # 'integracao-diaria-tenant-dc09e736': {
    #     'task': 'integrador.tasks.dispatcher_diario.sincronizar_diario',
    #     'schedule': crontab(hour=23, minute=5),
    #     'args': ('dc09e736-2ce2-41f1-a6a4-7a8c15d606df',),
    # },
}

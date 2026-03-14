from celery import shared_task
from django.core.cache import cache
from integrador.ssotica.workflows import workflow_diario, workflow_frequente

LOCK_EXPIRE = 3600

@shared_task
def executar_diario(tenant_id):
    if not cache.add(f"lock-ssotica-diario-{tenant_id}", "1", LOCK_EXPIRE):
        return "Lock ativo"
    workflow_diario(tenant_id).apply_async()


@shared_task
def executar_frequente(tenant_id):
    if not cache.add(f"lock-ssotica-frequente-{tenant_id}", "1", LOCK_EXPIRE):
        return "Lock ativo"
    workflow_frequente(tenant_id).apply_async()

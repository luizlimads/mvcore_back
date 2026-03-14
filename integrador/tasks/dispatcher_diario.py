import logging
from celery import shared_task
from tenant.models import Tenant
from integrador.registry import ERP_DIARIO_TASKS

logger = logging.getLogger(__name__)

@shared_task
def sincronizar_diario(tenant_id=None):

    tenants = (
        Tenant.objects.filter(id=tenant_id)
        if tenant_id
        else Tenant.objects.all()
    )

    count = 0
    for tenant in tenants:
        sistema = tenant.sistema_integrado.nome
        task = ERP_DIARIO_TASKS.get(sistema)

        if not task:
            continue

        task.delay(str(tenant.id))
        count+=1

    return f"Diario disparado para {count} tenants"

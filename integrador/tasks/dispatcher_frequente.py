from celery import shared_task
from tenant.models import Tenant
from integrador.registry import ERP_FREQUENTE_TASKS


@shared_task
def sincronizar_frequente(tenant_id=None):

    tenants = (
        Tenant.objects.filter(id=tenant_id)
        if tenant_id
        else Tenant.objects.all()
    )

    for tenant in tenants:
        sistema = tenant.sistema_integrado.nome
        task = ERP_FREQUENTE_TASKS.get(sistema)

        if not task:
            continue

        task.delay(str(tenant.id))

    return f"Frequente disparado para {tenants.count()} tenants"

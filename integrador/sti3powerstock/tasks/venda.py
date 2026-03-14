import logging
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from tenant.models import Tenant
from integrador.sti3powerstock.venda.importer import VendaImporter

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    max_retries=5,
    soft_time_limit=7200,
    time_limit=10000
)
def task_importar_venda(self, tenant_id):

    try:
        tenant = Tenant.objects.get(id=tenant_id)
        logger.info(f"[STi3PowerStock][Venda] Iniciando importação tenant={tenant_id}")

        VendaImporter(tenant=tenant).executar()

        logger.info(f"[STi3PowerStock][Venda] Concluída importação tenant={tenant_id}")

        return {
            "status": "ok",
            "tenant_id": tenant_id
        }

    except SoftTimeLimitExceeded:
        logger.warning(f"[STi3PowerStock][Venda] SoftTimeLimitExceeded tenant={tenant_id}, retry...")
        raise self.retry(countdown=2 ** self.request.retries * 60)

    except Exception as e:
        logger.exception(f"[STi3PowerStock][Venda] Erro ao importar tenant={tenant_id}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)

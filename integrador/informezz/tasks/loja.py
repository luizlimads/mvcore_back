import logging
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from tenant.models import Tenant
from integrador.informezz.loja.importer import LojaImporter

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    max_retries=5,
    soft_time_limit=7200,
    time_limit=10000
)
def task_importar_loja(self, tenant_id):

    try:
        tenant = Tenant.objects.get(id=tenant_id)
        logger.info(f"[Informezz][Loja] Iniciando importação para tenant={tenant_id}")

        LojaImporter(
            tenant=tenant.id,
            api_key=tenant.api_key
        ).executar()

        logger.info(f"[Informezz][Loja] Concluída importação tenant={tenant_id}")

        return {
            "status": "ok",
            "tenant_id": tenant_id
        }

    except SoftTimeLimitExceeded:
        logger.warning(f"[Informezz][Loja] SoftTimeLimitExceeded para tenant={tenant_id}, tentando retry...")
        raise self.retry(countdown=2 ** self.request.retries * 60)

    except Exception as e:
        logger.exception(f"[Informezz][Loja] Erro ao importar tenant={tenant_id}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)

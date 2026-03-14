import logging
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from tenant.models import Tenant
from integrador.ssotica.venda.importer import VendaImporter

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
        loja = tenant.lojas.first()

        if not loja:
            logger.warning(f"[SSÓtica][Venda] Tenant {tenant_id} não possui loja cadastrada. Ignorando.")
            return {"status": "sem_loja", "tenant_id": tenant_id}

        logger.info(f"[SSÓtica][Venda] Iniciando importação tenant={tenant_id}")

        VendaImporter(
            tenant=tenant.id,
            token=tenant.api_token,
            loja=loja.id,
            cnpj=tenant.api_document,
            aliquota=loja.imposto_aliquota_padrao
        ).executar()

        logger.info(f"[SSÓtica][Venda] Concluída importação tenant={tenant_id}")

        return {
            "status": "ok",
            "tenant_id": tenant_id
        }

    except SoftTimeLimitExceeded:
        logger.warning(f"[SSÓtica][Venda] SoftTimeLimitExceeded tenant={tenant_id}, retry...")
        raise self.retry(countdown=2 ** self.request.retries * 60)

    except Exception as e:
        logger.exception(f"[SSÓtica][Venda] Erro ao importar tenant={tenant_id}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)

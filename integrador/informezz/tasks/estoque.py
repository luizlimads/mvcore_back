import logging
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from tenant.models import Tenant
from integrador.informezz.estoque.importer import EstoqueImporter

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    max_retries=5,
    soft_time_limit=7200,
    time_limit=10000
)
def task_importar_estoque(self, tenant_id):
    try:
        tenant = Tenant.objects.get(id=tenant_id)

        importer = EstoqueImporter(
            tenant=tenant.id,
            api_key=tenant.api_key
        )

        logger.info(f"[Informezz][Estoque] Iniciando importação tenant={tenant_id}")
        importer.limpar_mes_corrente()

        total_pages = importer.obter_total_paginas()
        page_chunk_size = 50

        for start in range(1, total_pages + 1, page_chunk_size):
            end = min(start + page_chunk_size - 1, total_pages)

            logger.info(f"[Informezz][Estoque] Iniciando importação tenant={tenant_id} - Páginas: de {start} a {end}")
            importer.executar(start, end)
            logger.info(f"[Informezz][Estoque] Concluída importação tenant={tenant_id} - Páginas: de {start} a {end}")

        return {
            "status": "ok",
            "tenant_id": tenant_id
        }

    except SoftTimeLimitExceeded:
        logger.warning(
            f"[Informezz][Estoque] SoftTimeLimitExceeded tenant={tenant_id}, retry..."
        )
        raise self.retry(countdown=2 ** self.request.retries * 60)

    except Exception as e:
        logger.exception(
            f"[Informezz][Estoque] Erro ao importar tenant={tenant_id}"
        )
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)

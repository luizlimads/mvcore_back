from celery import chain, group
from .tasks.estoque import task_importar_estoque
from .tasks.venda import task_importar_venda
from .tasks.financeiro import task_importar_financeiro


def workflow_diario(tenant_id):
    return chain(
        task_importar_estoque.si(tenant_id),
        task_importar_venda.si(tenant_id),
        task_importar_financeiro.si(tenant_id),
    )

def workflow_frequente(tenant_id):
    return chain(
        group(
            task_importar_venda.si(tenant_id),
            task_importar_financeiro.si(tenant_id),
        )
    )

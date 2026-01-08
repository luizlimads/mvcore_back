from django.db import migrations
import uuid

def inserir_dados_iniciais(apps, schema_editor):
    SistemaIntegrado = apps.get_model('tenant', 'SistemaIntegrado')
    Tenant = apps.get_model('tenant', 'Tenant')

    # SISTEMA ADMIN
    admin_sistema_id = uuid.UUID('00000000-0000-0000-0000-000000000000')
    admin_sistema, _ = SistemaIntegrado.objects.get_or_create(
        id=admin_sistema_id,
        defaults={'nome': 'ADMIN'}
    )

    # TENANT ADMIN
    admin_tenant_id = uuid.UUID('00000000-0000-0000-0000-000000000000')
    Tenant.objects.get_or_create(
        id=admin_tenant_id,
        defaults={
            'documento': '00000000000',
            'razao_social': 'ADMIN',
            'sistema_integrado': admin_sistema
        }
    )

    # SISTEMA ssOtica
    ssotica_id = uuid.UUID('a84a2c72-03f7-4a0e-8ae6-b559400090d2')
    SistemaIntegrado.objects.get_or_create(
        id=ssotica_id,
        defaults={'nome': 'ssOtica'}
    )

class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(inserir_dados_iniciais),
    ]

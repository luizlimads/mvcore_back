from django.db import migrations
import uuid

def inserir_power_stock(apps, schema_editor):
    SistemaIntegrado = apps.get_model('tenant', 'SistemaIntegrado')
    
    # SISTEMA Power Stock
    powerstock_id = uuid.UUID('07b30bfd-f8c0-4d17-83c5-2c2955a6b2b7')
    SistemaIntegrado.objects.get_or_create(
        id=powerstock_id,
        defaults={'nome': 'STi3 - Power Stock'}
    )

class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0006_rename_documento_api_tenant_api_document_and_more'),
    ]

    operations = [
        migrations.RunPython(inserir_power_stock),
    ]

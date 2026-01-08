from django.db import migrations
import uuid

def inserir_informezz(apps, schema_editor):
    SistemaIntegrado = apps.get_model('tenant', 'SistemaIntegrado')
    
    # SISTEMA Informezz
    informezz_id = uuid.UUID('fdd72c28-d338-460b-9274-f3ad1cc863ea')
    SistemaIntegrado.objects.get_or_create(
        id=informezz_id,
        defaults={'nome': 'Informezz'}
    )

class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0008_loja_id_origem'),
    ]

    operations = [
        migrations.RunPython(inserir_informezz),
    ]

from django.db import migrations
from django.contrib.auth.hashers import make_password
import uuid

def create_admin_user(apps, schema_editor):
    User = apps.get_model('usuario', 'Usuario')
    Tenant = apps.get_model('tenant', 'Tenant')

    tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
    tenant = Tenant.objects.get(id=tenant_id)

    if not User.objects.filter(email='ti@maestriadovarejo.com').exists():
        User.objects.create(
            nome='admin',
            email='ti@maestriadovarejo.com',
            password=make_password('admin123'),
            is_superuser=True,
            is_staff=True,
            is_active=True,
            tenant=tenant
        )

class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]

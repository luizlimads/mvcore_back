from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_produto_cor_produto_departamento_produto_preco_custo_and_more'),
    ]

    operations = [
        migrations.RunSQL("DROP VIEW IF EXISTS vw_maestriabi_produtos;"),
        migrations.RunSQL("DROP VIEW IF EXISTS vw_maestriabi_estoques;"),
        migrations.RunSQL("DROP VIEW IF EXISTS vw_maestriabi_vendas;"),

        migrations.AlterField(
            model_name='estoque',
            name='cor',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='cor',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

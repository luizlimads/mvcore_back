from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0007_itemvenda_cor_itemvenda_tamanho'),
    ]

    operations = [
        migrations.RunSQL("DROP VIEW IF EXISTS vw_maestriabi_produtos;"),
        migrations.RunSQL("DROP VIEW IF EXISTS vw_maestriabi_estoques;"),
        migrations.RunSQL("DROP VIEW IF EXISTS vw_maestriabi_vendas;"),

        migrations.AlterField(
            model_name='itemvenda',
            name='cor',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

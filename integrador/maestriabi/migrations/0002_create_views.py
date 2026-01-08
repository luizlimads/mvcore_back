from django.db import migrations

VIEW_PRODUTOS = """
DROP VIEW IF EXISTS vw_maestriabi_produtos;
CREATE OR REPLACE VIEW vw_maestriabi_produtos AS
SELECT
    ROW_NUMBER() OVER (ORDER BY p.data_criacao) AS id,
    p.referencia as cod_produto,
    p.descricao as desc_produto,
    p.grupo as categoria,
    f.nome_fantasia as fornecedor,
    p.marca as nivel_1,
    'Sem Informação' as nivel_2,
    'Sem Informação' as nivel_3,
    p.tenant_id AS tenant_id
FROM produto_produtos p
LEFT JOIN (
    SELECT DISTINCT ON (fp.produto_id) fp.produto_id, f.nome_fantasia
    FROM fornecedor_fornecedores f
    INNER JOIN fornecedor_fornecedores_produtos fp ON f.id = fp.fornecedor_id
    ORDER BY fp.produto_id, f.data_criacao DESC
) f ON p.id = f.produto_id;
"""

VIEW_ESTOQUES = """
DROP VIEW IF EXISTS vw_maestriabi_estoques;
CREATE OR REPLACE VIEW vw_maestriabi_estoques AS
SELECT
    ROW_NUMBER() OVER (ORDER BY e.data_criacao) AS id,
    l.nome AS loja,
    (ARRAY[
        'JAN','FEV','MAR','ABR','MAI','JUN',
        'JUL','AGO','SET','OUT','NOV','DEZ'
    ])[EXTRACT(MONTH FROM e.data_criacao)::int] AS mes,
    EXTRACT(YEAR FROM e.data_criacao)::int AS ano,
    p.referencia AS codigo,
    COALESCE(i.imposto_aliquota, l.imposto_aliquota_padrao) as imposto,
    COALESCE(i.custo, 0) AS estoque_custo_unit,
    e.quantidade AS estoque_pecas,
    (COALESCE(i.custo, 0)*e.quantidade) AS custo_total,
    e.preco_venda AS estoque_vlr,
    date_trunc('month', e.data_criacao)::date AS data,
    l.tenant_id AS tenant_id
FROM produto_estoques e
INNER JOIN tenant_lojas l ON l.id = e.loja_id
INNER JOIN produto_produtos p ON p.id = e.produto_id
LEFT JOIN (
    SELECT
        DISTINCT ON (vi.produto_id)
        vi.produto_id,
        vi.custo,
        (vi.imposto_aliquota/100) AS imposto_aliquota
    FROM venda_itens vi
    ORDER BY vi.produto_id, vi.data_criacao DESC
) i ON p.id = i.produto_id;
"""

VIEW_VENDAS = """
DROP VIEW IF EXISTS vw_maestriabi_vendas;
CREATE OR REPLACE VIEW vw_maestriabi_vendas AS
SELECT
    ROW_NUMBER() OVER (ORDER BY v.data) AS id,
    l.nome as loja,
    (ARRAY[
        'JAN','FEV','MAR','ABR','MAI','JUN',
        'JUL','AGO','SET','OUT','NOV','DEZ'
    ])[EXTRACT(MONTH FROM v.data)::int] AS mes,
    EXTRACT(YEAR FROM v.data)::int AS ano,
    p.referencia AS codigo,
    (vi.custo*vi.quantidade) AS custo_total,
    vi.quantidade AS venda_qnt,
    vi.valor_total_liquido AS venda_vlr,
    vi.desconto AS descontos,
    v.numero AS venda,
    (vi.valor_unitario_liquido*vi.quantidade) AS vendas,
    ((vi.valor_unitario_liquido*vi.quantidade)-(vi.custo*vi.quantidade)) AS lucro_bruto,
    date_trunc('month', v.data)::date AS data,
    l.tenant_id AS tenant_id
FROM venda_vendas v
INNER JOIN tenant_lojas l ON l.id = v.loja_id
INNER JOIN venda_itens vi ON v.id = vi.venda_id
INNER JOIN produto_produtos p ON p.id = vi.produto_id;
"""

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('financeiro',  '0001_initial'),
        ('fornecedor',  '0001_initial'),
        ('funcionario', '0001_initial'),
        ('produto',     '0002_estoque_loja'),
        ('tenant',      '0005_remove_tenant_imposto_aliquota_padrao_and_more'),
        ('usuario',     '0001_initial'),
        ('venda',       '0004_alter_itemvenda_imposto_aliquota'),
        ('maestriabi',  '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(VIEW_PRODUTOS, reverse_sql="DROP VIEW IF EXISTS vw_maestriabi_produtos;"),
        migrations.RunSQL(VIEW_ESTOQUES, reverse_sql="DROP VIEW IF EXISTS vw_maestriabi_estoques;"),
        migrations.RunSQL(VIEW_VENDAS, reverse_sql="DROP VIEW IF EXISTS vw_maestriabi_vendas;"),
    ]

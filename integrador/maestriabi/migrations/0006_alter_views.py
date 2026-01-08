from django.db import migrations

VIEW_PRODUTOS = """
DROP VIEW IF EXISTS vw_maestriabi_produtos;
CREATE OR REPLACE VIEW public.vw_maestriabi_produtos AS
 SELECT row_number() OVER (ORDER BY p.data_criacao) AS id,
    (
		COALESCE(p.referencia, ''::character varying)::text ||
		COALESCE(p.id_origem, ''::character varying)::text ||
		COALESCE(e.cor, p.cor, ''::character varying)::text ||
		COALESCE(e.tamanho, p.tamanho, ''::character varying)::text
	) AS cod_produto,
    p.descricao AS desc_produto,
    p.grupo AS categoria,
    f.nome_fantasia AS fornecedor,
    p.marca AS nivel_1,
    CASE
		WHEN s.nome = 'Informezz' THEN COALESCE(p.colecao, 'Sem Informação'::character varying)
		ELSE COALESCE(e.cor, 'Sem Informação'::character varying)
	END AS nivel_2,
    COALESCE(e.tamanho, 'Sem Informação'::character varying) AS nivel_3,
    p.tenant_id
   FROM produto_produtos p
	 INNER JOIN tenant_tenants t ON p.tenant_id = t.id
	 INNER JOIN tenant_sistemas s ON t.sistema_integrado_id = s.id
     LEFT JOIN ( SELECT DISTINCT ON (fp.produto_id) fp.produto_id,
            COALESCE(NULLIF(f_1.nome_fantasia::text, ''::text), f_1.razao_social::text) AS nome_fantasia
           FROM fornecedor_fornecedores f_1
             JOIN fornecedor_fornecedores_produtos fp ON f_1.id = fp.fornecedor_id
          ORDER BY fp.produto_id, f_1.data_criacao DESC) f ON p.id = f.produto_id
     LEFT JOIN ( SELECT DISTINCT es.produto_id,
            es.cor,
            es.tamanho
           FROM produto_estoques es) e ON e.produto_id = p.id;
"""

VIEW_ESTOQUES = """
DROP VIEW IF EXISTS vw_maestriabi_estoques;
CREATE OR REPLACE VIEW public.vw_maestriabi_estoques AS
 SELECT row_number() OVER (ORDER BY e.data_criacao) AS id,
    l.nome AS loja,
    (ARRAY['JAN'::text, 'FEV'::text, 'MAR'::text, 'ABR'::text, 'MAI'::text, 'JUN'::text, 'JUL'::text, 'AGO'::text, 'SET'::text, 'OUT'::text, 'NOV'::text, 'DEZ'::text])[EXTRACT(month FROM e.data_criacao)::integer] AS mes,
    EXTRACT(year FROM e.data_criacao)::integer AS ano,
    ((COALESCE(p.referencia, ''::character varying)::text || COALESCE(p.id_origem, ''::character varying)::text) || COALESCE(e.cor, p.cor, ''::character varying)::text) || COALESCE(e.tamanho, p.tamanho, ''::character varying)::text AS codigo,
    COALESCE(i.imposto_aliquota, l.imposto_aliquota_padrao) AS imposto,
    COALESCE(i.custo, e.preco_custo::double precision, 0::double precision) AS estoque_custo_unit,
    e.quantidade AS estoque_pecas,
    COALESCE(i.custo, e.preco_custo::double precision, 0::double precision) * e.quantidade::double precision AS custo_total,
    e.preco_venda*e.quantidade AS estoque_vlr,
    date_trunc('month'::text, e.data_criacao)::date AS data,
    l.tenant_id
   FROM produto_estoques e
     JOIN tenant_lojas l ON l.id = e.loja_id
     JOIN produto_produtos p ON p.id = e.produto_id
     LEFT JOIN ( SELECT DISTINCT ON (vi.produto_id) vi.produto_id,
            vi.custo,
            vi.imposto_aliquota / 100::double precision AS imposto_aliquota
           FROM venda_itens vi
          ORDER BY vi.produto_id, vi.data_criacao DESC) i ON p.id = i.produto_id;
"""

VIEW_VENDAS = """
DROP VIEW IF EXISTS vw_maestriabi_vendas;
CREATE OR REPLACE VIEW public.vw_maestriabi_vendas AS
 SELECT row_number() OVER (ORDER BY v.data) AS id,
    l.nome AS loja,
    (ARRAY['JAN'::text, 'FEV'::text, 'MAR'::text, 'ABR'::text, 'MAI'::text, 'JUN'::text, 'JUL'::text, 'AGO'::text, 'SET'::text, 'OUT'::text, 'NOV'::text, 'DEZ'::text])[EXTRACT(month FROM v.data)::integer] AS mes,
    EXTRACT(year FROM v.data)::integer AS ano,
    ((COALESCE(p.referencia, ''::character varying)::text || COALESCE(p.id_origem, ''::character varying)::text) || COALESCE(vi.cor, p.cor, ''::character varying)::text) || COALESCE(vi.tamanho, p.tamanho, ''::character varying)::text AS codigo,
    vi.custo * vi.quantidade AS custo_total,
    vi.quantidade AS venda_qnt,
    vi.valor_total_liquido AS venda_vlr,
    vi.desconto AS descontos,
    COALESCE(v.numero, v.id_origem) AS venda,
    vi.valor_unitario_liquido * vi.quantidade AS vendas,
    vi.valor_unitario_liquido * vi.quantidade - vi.custo * vi.quantidade AS lucro_bruto,
    date_trunc('month'::text, v.data)::date AS data,
    l.tenant_id
   FROM venda_vendas v
     JOIN tenant_lojas l ON l.id = v.loja_id
     JOIN venda_itens vi ON v.id = vi.venda_id
     JOIN produto_produtos p ON p.id = vi.produto_id;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('maestriabi', '0005_alter_views'),
        ('produto', '0008_produto_colecao_produto_id_colecao_origem'),
        ('venda', '0009_itemvenda_funcionario'),
    ]

    operations = [
        migrations.RunSQL(VIEW_PRODUTOS, reverse_sql="DROP VIEW IF EXISTS vw_maestriabi_produtos;"),
        migrations.RunSQL(VIEW_ESTOQUES, reverse_sql="DROP VIEW IF EXISTS vw_maestriabi_estoques;"),
        migrations.RunSQL(VIEW_VENDAS, reverse_sql="DROP VIEW IF EXISTS vw_maestriabi_vendas;"),
    ]
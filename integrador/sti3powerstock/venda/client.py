import mysql.connector
from mysql.connector import Error

class VendaClient:
    def __init__(self, conf: dict):
        self.conf = conf

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.conf["host"],
            port=self.conf["port"],
            user=self.conf["user"],
            password=self.conf["password"],
            database=self.conf["database"],
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "conn") and self.conn.is_connected():
            self.conn.close()

    def fetch_dados(self, sql, params=None):
        try:
            with self.conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchall()
        except Error as e:
            raise RuntimeError(f"Erro ao buscar informações: {e}")

    def fetch_vendas(self, inicio_periodo, fim_periodo):
        return self.fetch_dados(
            """
                SELECT
                    v.codigo AS id_origem,
                    v.data_hora AS data,
                    v.status AS status,
                    v.codigo AS numero,
                    v.valortotal + v.desconto - v.acrescimo AS valor_bruto,
                    v.acrescimo AS acrescimo,
                    v.desconto AS desconto,
                    v.valortotal AS valor_liquido,
                    v.codvend AS funcionario,
                    v.codemp AS loja
                FROM vendas v
                WHERE v.data_hora BETWEEN %s AND %s
                ORDER BY v.data_hora;
            """,
            (inicio_periodo, fim_periodo)
        )

    def fetch_itens_por_vendas(self, venda_ids, chunk_size=800):
        if not venda_ids:
            return []

        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        resultados = []
        for chunk in chunks(venda_ids, chunk_size):
            placeholders = ",".join(["%s"] * len(chunk))
            sql = f"""
                SELECT
                    i.codempresa AS loja,
                    i.codvenda AS venda,
                    i.codprod AS produto,
                    i.codigo AS id_origem,
                    i.quantidade AS quantidade,
                    i.valorcusto AS custo,
                    i.valoravista AS valor_unitario_bruto,
                    i.desconto AS desconto,
                    i.acrescimo AS acrescimo,
                    (i.valortotalitem - i.desconto + i.acrescimo) / COALESCE(NULLIF(i.quantidade, 0), 1) AS valor_unitario_liquido,
                    (i.valortotalitem - i.desconto + i.acrescimo) AS valor_total_liquido,
                    (i.cancelado <> 0) AS cancelado,
                    t.descricao AS tamanho,
                    c.descricao AS cor
                FROM itens_vendas i
                LEFT JOIN tamanhos t ON i.codtam = t.codTamanho
                LEFT JOIN cores c ON i.Cor_idCor = c.codigo
                WHERE i.codvenda IN ({placeholders})
                ORDER BY i.codvenda;
            """
            resultados.extend(self.fetch_dados(sql, tuple(chunk)))
        return resultados

    def fetch_pagamentos_por_vendas(self, venda_ids, chunk_size=800):
        if not venda_ids:
            return []

        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        resultados = []
        for chunk in chunks(venda_ids, chunk_size):
            placeholders = ",".join(["%s"] * len(chunk))
            sql = f"""
                SELECT
                    cp.codvenda AS venda,
                    cp.codigo AS id_origem,
                    cp.dataemissao AS data,
                    cp.valor AS valor,
                    cp.parcela AS parcelas,
                    fp.descricao AS descricao
                FROM cond_pagto cp
                LEFT JOIN formapagto fp ON cp.codformapagto = fp.codigo
                WHERE cp.codvenda IN ({placeholders})
                ORDER BY cp.codvenda;
            """
            resultados.extend(self.fetch_dados(sql, tuple(chunk)))
        return resultados

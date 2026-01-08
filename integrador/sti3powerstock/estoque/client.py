import mysql.connector
from mysql.connector import Error

class EstoqueClient:
    def __init__(self, conf: dict):
        self.conf = conf

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.conf["host"],
            port=self.conf.get("port", 3306),
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

    def fetch_produtos(self, inicio_periodo, fim_periodo):
        return self.fetch_dados(
            """
            SELECT
                p.codpro AS id_origem,
                p.codpro AS referencia,
                p.descricao AS descricao,
                g.descricao AS grupo,
                p.codgrupo AS id_grupo_origem,
                m.descricao AS marca,
                p.codmarca AS id_marca_origem,
                p.dataultimaalteracao AS data_atualizacao_origem
            FROM produtos p
            LEFT JOIN grupos g ON p.codgrupo = g.codigo
            LEFT JOIN marcas m ON p.codmarca = m.codigo
            WHERE p.dataultimaalteracao BETWEEN %s AND %s
            ORDER BY p.dataultimaalteracao;
            """,
            (inicio_periodo, fim_periodo)
        )

    def fetch_estoques(self):
        return self.fetch_dados(
            """
            SELECT
                e.quantidade AS quantidade,
                e.precoavista AS preco_venda,
                e.precocusto AS preco_custo,
                t.descricao AS tamanho,
                c.descricao AS cor,
                e.codemp AS loja,
                e.codprod AS produto,
                e.datahoraatualizacao AS data_atualizacao_origem
            FROM estoque e
            LEFT JOIN tamanhos t ON e.codtam = t.codTamanho
            LEFT JOIN cores c ON e.Cor_idCor = c.codigo
            WHERE e.inativo = 0;
            """
        )

    def fetch_produtos_fornecedores(self):
        return self.fetch_dados(
            """
            SELECT
                pf.produtos_idprodutos AS produto,
                pf.fornecedores_idfornecedores AS fornecedor
            FROM produtofornecedornota pf;
            """
        )

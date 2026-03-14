import mysql.connector
from mysql.connector import Error
from tenant.models import Tenant

class EstoqueClient:
    def __init__(self, tenant: Tenant):
        self.tenant = tenant

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.tenant.db_host,
            port=self.tenant.db_port,
            user=self.tenant.db_user,
            password=self.tenant.db_pass,
            database=self.tenant.db_name
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
                    CAST(e.datahoraatualizacao AS CHAR) AS data_atualizacao_origem
                FROM estoque e
                LEFT JOIN tamanhos t ON e.codtam = t.codTamanho
                LEFT JOIN cores c ON e.Cor_idCor = c.codigo
                WHERE e.inativo = 0;
            """
        )

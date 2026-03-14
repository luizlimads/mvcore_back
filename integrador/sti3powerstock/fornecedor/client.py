import mysql.connector
from mysql.connector import Error
from tenant.models import Tenant

class FornecedorClient:
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

    def fetch_fornecedores(self):
        return self.fetch_dados(
            """
                SELECT
                    f.codigo AS id_origem,
                    REPLACE(REPLACE(REPLACE(f.cnpj, '.', ''), '-', ''), '/', '') AS documento,
                    NULLIF(f.razao, '') AS razao_social,
                    NULLIF(f.fantasia, '') AS nome_fantasia
                FROM fornecedores f;
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

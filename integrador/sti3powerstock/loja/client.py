import mysql.connector
from mysql.connector import Error
from tenant.models import Tenant

class LojaClient:
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

    def fetch_dados(self, sql):
        try:
            with self.conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except Error as e:
            raise RuntimeError(f"Erro ao buscar informações: {e}")

    def fetch_lojas(self):
        return self.fetch_dados(
            """
                SELECT
                    e.razao AS nome,
                    REPLACE(REPLACE(REPLACE(e.cnpj, '.', ''), '-', ''), '/', '') AS documento,
                    e.codigo AS id_origem
                FROM empresas e;
            """
        )

    def fetch_funcionarios(self):
        return self.fetch_dados(
            """
                SELECT
                    v.codigo AS id_origem,
                    NULLIF(v.nome, '') AS nome,
                    "Vendedor" AS funcao
                FROM vendedores v;
            """
        )
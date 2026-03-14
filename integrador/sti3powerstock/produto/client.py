import mysql.connector
from mysql.connector import Error
from tenant.models import Tenant
from django.utils import timezone

class ProdutoClient:
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

    def fetch_produtos(self, start_date):
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
                CAST(p.dataultimaalteracao AS CHAR) AS data_atualizacao_origem
            FROM produtos p
            LEFT JOIN grupos g ON p.codgrupo = g.codigo
            LEFT JOIN marcas m ON p.codmarca = m.codigo
            WHERE p.dataultimaalteracao BETWEEN %s AND %s
            ORDER BY p.dataultimaalteracao;
            """,
            (start_date, timezone.now().date())
        )

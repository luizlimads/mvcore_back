import mysql.connector
from mysql.connector import Error

class LojaClient:
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
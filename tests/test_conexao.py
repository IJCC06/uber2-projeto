import os
import unittest
from unittest.mock import patch

import conexao


class CriarConexaoTests(unittest.TestCase):
    def test_prefere_database_url_quando_configurada(self):
        database_url = "postgresql://usuario:senha@example.neon.tech/banco"
        with patch.dict(os.environ, {"DATABASE_URL": database_url}, clear=True):
            with patch("conexao.psycopg2.connect") as connect:
                conexao.criar_conexao()

        connect.assert_called_once_with(database_url)

    def test_preserva_configuracao_local_db(self):
        config = {
            "DB_HOST": "localhost",
            "DB_NAME": "uber2_v2",
            "DB_USER": "usuario",
            "DB_PASSWORD": "senha",
        }
        with patch.dict(os.environ, config, clear=True):
            with patch("conexao.psycopg2.connect") as connect:
                conexao.criar_conexao()

        connect.assert_called_once_with(
            host="localhost",
            database="uber2_v2",
            user="usuario",
            password="senha",
        )


if __name__ == "__main__":
    unittest.main()

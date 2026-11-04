import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def criar_conexao():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "A variável DATABASE_URL não foi definida no arquivo .env."
        )

    return psycopg.connect(database_url)

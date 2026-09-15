import sqlite3

CAMINHO_BANCO = "../database/uber2.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    # Permite utilizar as chaves estrangeiras no SQLite
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao
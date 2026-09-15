import sqlite3

CAMINHO_BANCO = "../database/uber2.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao
import sqlite3
import os


def conectar():
    caminho = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "uber2.db"
    )

    conexao = sqlite3.connect(caminho)
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao
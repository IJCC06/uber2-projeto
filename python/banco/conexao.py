import sqlite3
import os

print(">>> conexao.py foi carregado!")

def conectar():
    caminho = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "uber2.db"
    )

    print(">>> BANCO USADO:", caminho)

    conexao = sqlite3.connect(caminho)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao
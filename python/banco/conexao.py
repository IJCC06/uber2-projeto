import sqlite3
import os
import sys


def conectar():
    if getattr(sys, "frozen", False):
        pasta_projeto = os.path.dirname(sys.executable)
    else:
        pasta_projeto = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

    caminho = os.path.join(pasta_projeto, "uber2.db")

    conexao = sqlite3.connect(caminho)
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao
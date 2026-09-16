import sqlite3


def conectar():
    conexao = sqlite3.connect("../uber2.db")

    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao
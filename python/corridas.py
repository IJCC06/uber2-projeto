import sqlite3
from conexao import conectar


def cadastrar_corrida(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    id_origem = input("Digite o ID do endereço de origem: ")
    id_destino = input("Digite o ID do endereço de destino: ")
    valor = input("Digite o valor da corrida: ")

    try:
        cursor.execute("""
            INSERT INTO corridas
            (id_usuario, id_origem, id_destino, valor)
            VALUES (?, ?, ?, ?)
        """, (id_usuario, id_origem, id_destino, valor))

        conexao.commit()
        print("Corrida cadastrada com sucesso!")

    except sqlite3.IntegrityError:
        print("Não foi possível cadastrar a corrida.")

    conexao.close()
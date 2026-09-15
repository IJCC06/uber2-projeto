import sqlite3
from conexao import conectar


def cadastrar_avaliacao(id_corrida):
    conexao = conectar()
    cursor = conexao.cursor()

    nota = input("Digite a nota da corrida (1 a 5): ")
    comentario = input("Digite um comentário sobre a corrida: ")

    try:
        cursor.execute("""
            INSERT INTO avaliacoes
            (id_corrida, nota, comentario)
            VALUES (?, ?, ?)
        """, (id_corrida, nota, comentario))

        conexao.commit()
        print("Avaliação cadastrada com sucesso!")

    except sqlite3.IntegrityError:
        print("Não foi possível cadastrar a avaliação.")

    conexao.close()
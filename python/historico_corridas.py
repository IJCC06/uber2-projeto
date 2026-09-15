import sqlite3
from conexao import conectar


def registrar_historico(id_corrida, status_anterior, novo_status):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO historico_corridas
            (id_corrida, status_anterior, novo_status)
            VALUES (?, ?, ?)
        """, (id_corrida, status_anterior, novo_status))

        conexao.commit()
        print("Histórico registrado com sucesso!")

    except sqlite3.IntegrityError:
        print("Não foi possível registrar o histórico.")

    conexao.close()
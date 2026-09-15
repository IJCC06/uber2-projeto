import sqlite3
from conexao import conectar


def cadastrar_pagamento(id_corrida):
    conexao = conectar()
    cursor = conexao.cursor()

    forma_pagamento = input("Digite a forma de pagamento (Pix, Dinheiro ou Cartão): ")
    valor = input("Digite o valor do pagamento: ")

    try:
        cursor.execute("""
            INSERT INTO pagamentos
            (id_corrida, forma_pagamento, valor)
            VALUES (?, ?, ?)
        """, (id_corrida, forma_pagamento, valor))

        conexao.commit()
        print("Pagamento cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        print("Não foi possível cadastrar o pagamento.")

    conexao.close()
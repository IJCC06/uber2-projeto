import sqlite3
from conexao import conectar


def cadastrar_veiculo(id_motorista):
    conexao = conectar()
    cursor = conexao.cursor()

    modelo = input("Digite o modelo do veículo: ")
    marca = input("Digite a marca do veículo: ")
    placa = input("Digite a placa do veículo: ")
    ano = input("Digite o ano do veículo: ")
    cor = input("Digite a cor do veículo: ")

    try:
        cursor.execute("""
            INSERT INTO veiculos
            (id_motorista, modelo, marca, placa, ano, cor)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_motorista, modelo, marca, placa, ano, cor))

        conexao.commit()
        print("Veículo cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        print("Não foi possível cadastrar o veículo.")

    conexao.close()
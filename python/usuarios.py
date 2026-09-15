import sqlite3
from conexao import conectar

def cadastrar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()

    nome = input("Digite seu nome completo: ")
    email = input("Digite seu email: ")
    print("Para o telefone siga este modelo --> (xx) xxxxx-xxxx")
    telefone = input("Digite seu telefone com DDD: ")
    print("Sua senha deverá conter apenas alfanúmericos (letras e números)")
    senha = input("Digite sua senha: ")

    if not nome or email or telefone or senha:
        print("")

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, email, telefone, senha)
            VALUES (?, ?, ?, ?)
        """, (nome, email, telefone, senha))

        conexao.commit()

    except sqlite3.IntegrityError:
        print("Este e-mail já está cadastrado!")

    conexao.close()
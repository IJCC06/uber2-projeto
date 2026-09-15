import sqlite3
from conexao import conectar

def cadastrar_usuario():
    conexao = conectar()
    cursor = conexao.cursor()

    nome = input("Digite seu nome completo: ")
    email = input("Digite seu email: ")
    print("Para o telefone siga este modelo --> (xx) xxxxx-xxxx")
    telefone = input("Digite seu telefone com DDD: ")
    print("Sua senha deverá conter apenas alfanúmericos (letras e números)")
    senha = input("Digite sua senha: ")

    if not nome or not email or not telefone or not senha:
        print("Preencha todos os campos")
        conexao.close()
        return

    if not senha.isalnum():
        print("A senha deve conter apenas letras e números")
        conexao.close()
        return

    if not any(caractere.isalpha() for caractere in senha) or not any(caractere.isdigit() for caractere in senha):
        print("A senha deve conter pelo menos uma letra e um número.")
        conexao.close()
        return

    if "@" not in email or "." not in email:
        print("Digite um e-mail válido.")
        conexao.close()
        return

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, email, telefone, senha)
            VALUES (?, ?, ?, ?)
        """, (nome, email, telefone, senha))

        conexao.commit()
        print("Usuário cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        print("Este e-mail já está cadastrado!")

    conexao.close()
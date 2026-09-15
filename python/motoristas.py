from conexao import conectar

def cadastrar_motorista():
    conexao = conectar()
    cursor = conexao.cursor()

    nome = input("Insira o Nome: ")
    cpf = input("Insira o CPF: ")
    telefone = input("Insira o Telefone: ")
    cnh = input("Insira a CNH")

    cursor.execute("""
        INSERT INTO motoristas (nome, cpf, telefone, cnh)
        VALUES (?, ?, ?, ?)
    """, (nome, cpf, telefone, cnh))

    conexao.commit()
    print("Motorista cadastrado com sucesso!")
    conexao.close()
from conexao import conectar

def cadastrar_motorista():
    conexao = conectar()
    cursor = conexao.cursor()

    nome = input("Insira o Nome: ")
    cpf = input("Insira o CPF: ")
    telefone = input("Insira o Telefone: ")
    cnh = input("Insira a CNH")

cadastrar_motorista()
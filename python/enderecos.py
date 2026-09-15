from conexao import conectar

def cadastrar_enderecos():
    conexao = conectar()
    cursor = conexao.cursor()

    rua = input("Digite a rua: ")
    numero = input("Digite o número: ")
    bairro = input("Digite o bairro: ")
    cidade = input("Digite a cidade: ")
    estado = input("Digite o estado: ")
    cep = input("Digite o CEP: ")

    cursor.execute("""
        INSERT INTO enderecos
        (rua, numero, bairro, cidade, estado, cep)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (rua, numero, bairro, cidade, estado, cep))

    conexao.commit()
    print("Endereço cadastrado com sucesso!")

    conexao.close()
from conexao import conectar

def mostrar_colunas(tabela):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(f"PRAGMA table_info({tabela})")

    colunas = cursor.fetchall()

    print(f"Colunas da tabela '{tabela}':")

    for coluna in colunas:
        print("-", coluna[1])

    conexao.close()


mostrar_colunas("usuarios")
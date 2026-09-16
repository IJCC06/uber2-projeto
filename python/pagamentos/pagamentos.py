from banco.conexao import conectar

# Cadastrar o Pagamento (Usuario)
def cadastrar_pagamento(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    id_corrida = int(input("Digite o ID da corrida que deseja pagar: "))

    cursor.execute("""
        SELECT valor, status
        FROM corridas
        WHERE id = ?
          AND id_usuario = ?
    """, (id_corrida, id_usuario))

    corrida = cursor.fetchone()

    if corrida is None:
        print("Corrida não encontrada ou não pertence a você.")
        conexao.close()
        return

    valor = corrida[0]
    status_corrida = corrida[1]

    # Só dá para pagar uma corrida finalizada
    if status_corrida != "Finalizada":
        print("Só é possível pagar uma corrida finalizada.")
        conexao.close()
        return

    if valor is None:
        print("Esta corrida não possui um valor definido.")
        conexao.close()
        return

    cursor.execute("""
        SELECT id
        FROM pagamentos
        WHERE id_corrida = ?
    """, (id_corrida,))

    pagamento = cursor.fetchone()

    if pagamento is not None:
        print("Esta corrida já possui um pagamento cadastrado.")
        conexao.close()
        return

    print("\n--- FORMA DE PAGAMENTO ---")
    print("1 - Pix")
    print("2 - Dinheiro")
    print("3 - Cartão")

    opcao = input("Escolha a forma de pagamento: ")

    formas_pagamento = {
        "1": "Pix",
        "2": "Dinheiro",
        "3": "Cartão"
    }

    if opcao not in formas_pagamento:
        print("Opção inválida.")
        conexao.close()
        return

    forma_pagamento = formas_pagamento[opcao]

    cursor.execute("""
        INSERT INTO pagamentos (
            id_corrida,
            forma_pagamento,
            valor,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        id_corrida,
        forma_pagamento,
        valor,
        "Pago"
    ))

    conexao.commit()
    conexao.close()

    print("Pagamento cadastrado com sucesso!")


# Listar Pagamentos do Usuário
def listar_pagamentos_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            pagamentos.id,
            pagamentos.id_corrida,
            pagamentos.forma_pagamento,
            pagamentos.valor,
            pagamentos.status,
            pagamentos.data_pagamento
        FROM pagamentos
        INNER JOIN corridas
            ON pagamentos.id_corrida = corridas.id
        WHERE corridas.id_usuario = ?
        ORDER BY pagamentos.id DESC
    """, (id_usuario,))

    pagamentos = cursor.fetchall()

    conexao.close()

    if not pagamentos:
        print("\nVocê ainda não possui pagamentos.")
        return

    print("\n========== MEUS PAGAMENTOS ==========")

    for pagamento in pagamentos:
        print(f"ID do pagamento: {pagamento[0]}")
        print(f"ID da corrida: {pagamento[1]}")
        print(f"Forma de pagamento: {pagamento[2]}")
        print(f"Valor: R$ {pagamento[3]:.2f}")
        print(f"Status: {pagamento[4]}")
        print(f"Data do pagamento: {pagamento[5]}")
        print("-------------------------------------")


# Listar todos os pagamentos por usuário (ADM)
def listar_pagamentos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            pagamentos.id,
            pagamentos.id_corrida,
            usuarios.nome,
            pagamentos.forma_pagamento,
            pagamentos.valor,
            pagamentos.status,
            pagamentos.data_pagamento
        FROM pagamentos
        INNER JOIN corridas
            ON pagamentos.id_corrida = corridas.id
        INNER JOIN usuarios
            ON corridas.id_usuario = usuarios.id
        ORDER BY pagamentos.id
    """)

    pagamentos = cursor.fetchall()

    conexao.close()

    if not pagamentos:
        print("\nNenhum pagamento cadastrado.")
        return

    print("\n========== TODOS OS PAGAMENTOS ==========")

    for pagamento in pagamentos:
        print(f"ID do pagamento: {pagamento[0]}")
        print(f"ID da corrida: {pagamento[1]}")
        print(f"Usuário: {pagamento[2]}")
        print(f"Forma de pagamento: {pagamento[3]}")
        print(f"Valor: R$ {pagamento[4]:.2f}")
        print(f"Status: {pagamento[5]}")
        print(f"Data do pagamento: {pagamento[6]}")
        print("----------------------------------------")


# Editar Pagamento (ADM)
def editar_pagamento():
    conexao = conectar()
    cursor = conexao.cursor()

    id_pagamento = int(input("Digite o ID do pagamento que deseja editar: "))

    cursor.execute("""
        SELECT forma_pagamento, valor, status
        FROM pagamentos
        WHERE id = ?
    """, (id_pagamento,))

    pagamento = cursor.fetchone()

    if pagamento is None:
        print("Pagamento não encontrado.")
        conexao.close()
        return

    print("\n--- EDITAR PAGAMENTO ---")
    print("Deixe vazio para manter o valor atual.\n")

    print(f"Forma atual: {pagamento[0]}")
    print(f"Valor atual: R$ {pagamento[1]:.2f}")
    print(f"Status atual: {pagamento[2]}")

    print("\nFormas de pagamento:")
    print("1 - Pix")
    print("2 - Dinheiro")
    print("3 - Cartão")

    forma = input("Nova forma de pagamento [Enter para manter]: ")

    if forma == "":
        nova_forma = pagamento[0]
    else:
        formas_pagamento = {
            "1": "Pix",
            "2": "Dinheiro",
            "3": "Cartão"
        }

        if forma not in formas_pagamento:
            print("Forma de pagamento inválida.")
            conexao.close()
            return

        nova_forma = formas_pagamento[forma]

    valor = input(f"Novo valor [{pagamento[1]}]: ")

    if valor == "":
        novo_valor = pagamento[1]
    else:
        novo_valor = float(valor)

        if novo_valor < 0:
            print("O valor não pode ser negativo.")
            conexao.close()
            return

    print("\nStatus:")
    print("1 - Pendente")
    print("2 - Pago")
    print("3 - Cancelado")

    status = input("Novo status [Enter para manter]: ")

    if status == "":
        novo_status = pagamento[2]
    else:
        status_pagamento = {
            "1": "Pendente",
            "2": "Pago",
            "3": "Cancelado"
        }

        if status not in status_pagamento:
            print("Status inválido.")
            conexao.close()
            return

        novo_status = status_pagamento[status]

    cursor.execute("""
        UPDATE pagamentos
        SET forma_pagamento = ?,
            valor = ?,
            status = ?
        WHERE id = ?
    """, (
        nova_forma,
        novo_valor,
        novo_status,
        id_pagamento
    ))

    conexao.commit()
    conexao.close()

    print("Pagamento atualizado com sucesso!")


# Excluir Pagamento (ADM)
def excluir_pagamento():
    conexao = conectar()
    cursor = conexao.cursor()

    id_pagamento = int(input("Digite o ID do pagamento que deseja excluir: "))

    cursor.execute("""
        SELECT id_corrida, forma_pagamento, valor, status
        FROM pagamentos
        WHERE id = ?
    """, (id_pagamento,))

    pagamento = cursor.fetchone()

    if pagamento is None:
        print("Pagamento não encontrado.")
        conexao.close()
        return

    print("\n--- PAGAMENTO SELECIONADO ---")
    print(f"ID da corrida: {pagamento[0]}")
    print(f"Forma de pagamento: {pagamento[1]}")
    print(f"Valor: R$ {pagamento[2]:.2f}")
    print(f"Status: {pagamento[3]}")

    confirmacao = input(
        "\nTem certeza que deseja excluir este pagamento? (S/N): "
    )

    if confirmacao.upper() != "S":
        print("Exclusão cancelada.")
        conexao.close()
        return

    cursor.execute("""
        DELETE FROM pagamentos
        WHERE id = ?
    """, (id_pagamento,))

    conexao.commit()
    conexao.close()

    print("Pagamento excluído com sucesso!")
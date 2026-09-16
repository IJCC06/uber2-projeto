from banco.conexao import conectar
from historico.historico import registrar_historico

# Cadastrar Corrida (Usuário)
def cadastrar_corrida(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    origem = input("Insira o endereço de origem: ")
    destino = input("Insira o endereço de destino: ")

    if origem == destino:
        print("A origem e o destino não podem ser iguais.")
        conexao.close()
        return

    cursor.execute("""
        INSERT INTO corridas (
            id_usuario,
            origem,
            destino
        )
        VALUES (?, ?, ?)
    """, (
        id_usuario,
        origem,
        destino
    ))

    conexao.commit()
    conexao.close()

    print("Corrida solicitada com sucesso!")


# Listar Corridas (Usuários)
def listar_corridas_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            corridas.id,
            corridas.origem,
            corridas.destino,
            corridas.data_hora,
            corridas.valor,
            corridas.status,
            motoristas.nome
        FROM corridas
        LEFT JOIN motoristas
            ON corridas.id_motorista = motoristas.id
        WHERE corridas.id_usuario = ?
        ORDER BY corridas.id DESC
    """, (id_usuario,))

    corridas = cursor.fetchall()

    conexao.close()

    if not corridas:
        print("\nVocê ainda não possui corridas.")
        return

    print("\n========== MINHAS CORRIDAS ==========")

    for corrida in corridas:
        print(f"ID: {corrida[0]}")
        print(f"Origem: {corrida[1]}")
        print(f"Destino: {corrida[2]}")
        print(f"Data e hora: {corrida[3]}")
        print(f"Valor: {corrida[4]}")
        print(f"Status: {corrida[5]}")

        if corrida[6] is None:
            print("Motorista: Ainda não atribuído")
        else:
            print(f"Motorista: {corrida[6]}")

        print("-------------------------------------")


# Listar Corridas Disponíveis (Motoristas)
def listar_corridas_disponiveis():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            corridas.id,
            usuarios.nome,
            corridas.origem,
            corridas.destino,
            corridas.data_hora
        FROM corridas
        INNER JOIN usuarios
            ON corridas.id_usuario = usuarios.id
        WHERE corridas.status = 'Solicitada'
          AND corridas.id_motorista IS NULL
        ORDER BY corridas.id
    """)

    corridas = cursor.fetchall()

    conexao.close()

    if not corridas:
        print("\nNão há corridas disponíveis no momento.")
        return

    print("\n========== CORRIDAS DISPONÍVEIS ==========")

    for corrida in corridas:
        print(f"ID: {corrida[0]}")
        print(f"Usuário: {corrida[1]}")
        print(f"Origem: {corrida[2]}")
        print(f"Destino: {corrida[3]}")
        print(f"Data e hora: {corrida[4]}")
        print("------------------------------------------")


# Aceitar Corrida (Motorista)
def aceitar_corrida(id_motorista):
    conexao = conectar()
    cursor = conexao.cursor()

    id_corrida = int(input("Digite o ID da corrida que deseja aceitar: "))

    cursor.execute("""
        SELECT status, id_motorista
        FROM corridas
        WHERE id = ?
    """, (id_corrida,))

    corrida = cursor.fetchone()

    if not corrida:
        print("\nCorrida não encontrada.")
        conexao.close()
        return

    status_atual = corrida[0]
    motorista_atual = corrida[1]

    if status_atual != "Solicitada" or motorista_atual is not None:
        print("\nEssa corrida não está disponível para ser aceita.")
        conexao.close()
        return

    cursor.execute("""
        UPDATE corridas
        SET id_motorista = ?,
            status = 'Aceita'
        WHERE id = ?
          AND status = 'Solicitada'
          AND id_motorista IS NULL
    """, (id_motorista, id_corrida))

    if cursor.rowcount == 0:
        print("\nNão foi possível aceitar a corrida.")
        conexao.close()
        return

    conexao.commit()
    conexao.close()

    registrar_historico(
        id_corrida,
        status_atual,
        "Aceita"
    )

    print("\nCorrida aceita com sucesso!")


# Atualizar Status de Corrida (Motorista)
def atualizar_status_corrida(id_motorista):
    conexao = conectar()
    cursor = conexao.cursor()

    id_corrida = int(input("Digite o ID da corrida: "))

    cursor.execute("""
        SELECT status
        FROM corridas
        WHERE id = ?
          AND id_motorista = ?
    """, (id_corrida, id_motorista))

    corrida = cursor.fetchone()

    if not corrida:
        print("\nCorrida não encontrada ou não pertence a você.")
        conexao.close()
        return

    status_atual = corrida[0]

    if status_atual == "Aceita":
        print("\n1 - Em andamento")
        print("2 - Cancelada")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            novo_status = "Em andamento"
        elif opcao == "2":
            novo_status = "Cancelada"
        else:
            print("\nOpção inválida.")
            conexao.close()
            return

    elif status_atual == "Em andamento":
        print("\n1 - Finalizada")
        print("2 - Cancelada")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            novo_status = "Finalizada"
        elif opcao == "2":
            novo_status = "Cancelada"
        else:
            print("\nOpção inválida.")
            conexao.close()
            return

    else:
        print("\nEssa corrida não pode mais ter o status alterado.")
        conexao.close()
        return

    cursor.execute("""
        UPDATE corridas
        SET status = ?
        WHERE id = ?
          AND id_motorista = ?
    """, (novo_status, id_corrida, id_motorista))

    # Testa as Linha Alteradas pelo UPDATE acima
    if cursor.rowcount == 0:
        print("\nNão foi possível atualizar a corrida.")
        conexao.close()
        return

    conexao.commit()
    conexao.close()

    registrar_historico(
        id_corrida,
        status_atual,
        novo_status
    )

    print("\nStatus da corrida atualizado com sucesso!")


# Listar todas as Corridas (ADM)
def listar_todas_corridas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            corridas.id,
            usuarios.nome,
            motoristas.nome,
            corridas.origem,
            corridas.destino,
            corridas.data_hora,
            corridas.valor,
            corridas.status
        FROM corridas
        INNER JOIN usuarios
            ON corridas.id_usuario = usuarios.id
        LEFT JOIN motoristas
            ON corridas.id_motorista = motoristas.id
        ORDER BY corridas.id
    """)

    corridas = cursor.fetchall()

    conexao.close()

    if not corridas:
        print("\nNenhuma corrida cadastrada.")
        return

    print("\n========== TODAS AS CORRIDAS ==========")

    for corrida in corridas:
        print(f"ID: {corrida[0]}")
        print(f"Usuário: {corrida[1]}")

        if corrida[2] is None:
            print("Motorista: Ainda não atribuído")
        else:
            print(f"Motorista: {corrida[2]}")

        print(f"Origem: {corrida[3]}")
        print(f"Destino: {corrida[4]}")
        print(f"Data e hora: {corrida[5]}")
        print(f"Valor: {corrida[6]}")
        print(f"Status: {corrida[7]}")
        print("---------------------------------------")


# Editar Corrida (ADM)
def editar_corrida():
    conexao = conectar()
    cursor = conexao.cursor()

    id_corrida = int(input("Digite o ID da corrida que deseja editar: "))

    cursor.execute("""
        SELECT origem, destino, valor, status
        FROM corridas
        WHERE id = ?
    """, (id_corrida,))

    corrida = cursor.fetchone()

    if corrida is None:
        print("Corrida não encontrada.")
        conexao.close()
        return

    print("\n--- EDITAR CORRIDA ---")
    print("Deixe vazio para manter o valor atual.\n")

    origem = input(f"Origem [{corrida[0]}]: ")
    destino = input(f"Destino [{corrida[1]}]: ")
    valor = input(f"Valor [{corrida[2]}]: ")
    status = input(f"Status [{corrida[3]}]: ")

    if origem == "":
        origem = corrida[0]

    if destino == "":
        destino = corrida[1]

    if origem == destino:
        print("A origem e o destino não podem ser iguais.")
        conexao.close()
        return

    if valor == "":
        valor = corrida[2]
    else:
        valor = float(valor)

    if status == "":
        status = corrida[3]

    status_validos = (
        "Solicitada",
        "Aceita",
        "Em andamento",
        "Finalizada",
        "Cancelada"
    )

    if status not in status_validos:
        print("Status inválido.")
        conexao.close()
        return

    cursor.execute("""
        UPDATE corridas
        SET origem = ?,
            destino = ?,
            valor = ?,
            status = ?
        WHERE id = ?
    """, (
        origem,
        destino,
        valor,
        status,
        id_corrida
    ))

    conexao.commit()
    conexao.close()

    print("Corrida atualizada com sucesso!")


# Excluir Corrida (ADM)
def excluir_corrida():
    conexao = conectar()
    cursor = conexao.cursor()

    id_corrida = int(input("Digite o ID da corrida que deseja excluir: "))

    cursor.execute("""
        SELECT origem, destino, status
        FROM corridas
        WHERE id = ?
    """, (id_corrida,))

    corrida = cursor.fetchone()

    if corrida is None:
        print("Corrida não encontrada.")
        conexao.close()
        return

    print("\n--- CORRIDA SELECIONADA ---")
    print(f"Origem: {corrida[0]}")
    print(f"Destino: {corrida[1]}")
    print(f"Status: {corrida[2]}")

    confirmacao = input(
        "Tem certeza que deseja excluir esta corrida? (S/N): "
    )

    if confirmacao.upper() != "S":
        print("Exclusão cancelada.")
        conexao.close()
        return

    cursor.execute("""
        SELECT COUNT(*)
        FROM pagamentos
        WHERE id_corrida = ?
    """, (id_corrida,))

    quantidade_pagamentos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM avaliacoes
        WHERE id_corrida = ?
    """, (id_corrida,))

    quantidade_avaliacoes = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM historico_corridas
        WHERE id_corrida = ?
    """, (id_corrida,))

    quantidade_historico = cursor.fetchone()[0]

    if (
        quantidade_pagamentos > 0
        or quantidade_avaliacoes > 0
        or quantidade_historico > 0
    ):
        print("Não é possível excluir esta corrida.")
        print("Ela possui registros relacionados.")
        conexao.close()
        return

    cursor.execute("""
        DELETE FROM corridas
        WHERE id = ?
    """, (id_corrida,))

    conexao.commit()
    conexao.close()

    print("Corrida excluída com sucesso!")
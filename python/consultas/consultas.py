from banco.conexao import conectar


def cinco_corridas_mais_caras():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            corridas.id,
            usuarios.nome,
            motoristas.nome,
            corridas.origem,
            corridas.destino,
            corridas.valor
        FROM corridas
        INNER JOIN usuarios
            ON corridas.id_usuario = usuarios.id
        LEFT JOIN motoristas
            ON corridas.id_motorista = motoristas.id
        WHERE corridas.valor IS NOT NULL
        ORDER BY corridas.valor DESC
        LIMIT 5
    """)

    corridas = cursor.fetchall()

    conexao.close()

    if not corridas:
        print("\nNenhuma corrida com valor encontrada.")
        return

    print("\n========== 5 CORRIDAS MAIS CARAS ==========")

    for corrida in corridas:
        print(f"ID da corrida: {corrida[0]}")
        print(f"Usuário: {corrida[1]}")
        print(f"Motorista: {corrida[2] if corrida[2] else 'Não atribuído'}")
        print(f"Origem: {corrida[3]}")
        print(f"Destino: {corrida[4]}")
        print(f"Valor: R$ {corrida[5]:.2f}")
        print("-------------------------------------------")


def motorista_mais_corridas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            motoristas.id,
            motoristas.nome,
            COUNT(corridas.id) AS quantidade_corridas
        FROM motoristas
        INNER JOIN corridas
            ON motoristas.id = corridas.id_motorista
        GROUP BY motoristas.id, motoristas.nome
        ORDER BY quantidade_corridas DESC
        LIMIT 1
    """)

    motorista = cursor.fetchone()

    conexao.close()

    if not motorista:
        print("\nNenhum motorista possui corridas.")
        return

    print("\n========== MOTORISTA COM MAIS CORRIDAS ==========")
    print(f"ID do motorista: {motorista[0]}")
    print(f"Nome: {motorista[1]}")
    print(f"Quantidade de corridas: {motorista[2]}")


def forma_pagamento_mais_utilizada():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            forma_pagamento,
            COUNT(*) AS quantidade
        FROM pagamentos
        GROUP BY forma_pagamento
        ORDER BY quantidade DESC
        LIMIT 1
    """)

    forma = cursor.fetchone()

    conexao.close()

    if not forma:
        print("\nNenhum pagamento encontrado.")
        return

    print("\n========== FORMA DE PAGAMENTO MAIS UTILIZADA ==========")
    print(f"Forma de pagamento: {forma[0]}")
    print(f"Quantidade de pagamentos: {forma[1]}")


def usuarios_mais_corridas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            usuarios.id,
            usuarios.nome,
            COUNT(corridas.id) AS quantidade_corridas
        FROM usuarios
        INNER JOIN corridas
            ON usuarios.id = corridas.id_usuario
        GROUP BY usuarios.id, usuarios.nome
        ORDER BY quantidade_corridas DESC
    """)

    usuarios = cursor.fetchall()

    conexao.close()

    if not usuarios:
        print("\nNenhum usuário possui corridas.")
        return

    print("\n========== USUÁRIOS COM MAIS CORRIDAS ==========")

    for usuario in usuarios:
        print(f"ID: {usuario[0]}")
        print(f"Nome: {usuario[1]}")
        print(f"Quantidade de corridas: {usuario[2]}")
        print("-----------------------------------------------")


def motoristas_disponiveis():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            cpf,
            telefone,
            cnh
        FROM motoristas
        WHERE status = 'Ativo'
        ORDER BY nome
    """)

    motoristas = cursor.fetchall()

    conexao.close()

    if not motoristas:
        print("\nNenhum motorista ativo encontrado.")
        return

    print("\n========== MOTORISTAS DISPONÍVEIS ==========")

    for motorista in motoristas:
        print(f"ID: {motorista[0]}")
        print(f"Nome: {motorista[1]}")
        print(f"CPF: {motorista[2]}")
        print(f"Telefone: {motorista[3]}")
        print(f"CNH: {motorista[4]}")
        print("--------------------------------------------")


def historico_determinada_corrida():
    conexao = conectar()
    cursor = conexao.cursor()

    id_corrida = int(input("Digite o ID da corrida: "))

    cursor.execute("""
        SELECT
            historico_corridas.id,
            historico_corridas.id_corrida,
            historico_corridas.status_anterior,
            historico_corridas.novo_status,
            historico_corridas.data_alteracao
        FROM historico_corridas
        WHERE historico_corridas.id_corrida = ?
        ORDER BY historico_corridas.id
    """, (id_corrida,))

    historico = cursor.fetchall()

    conexao.close()

    if not historico:
        print("\nNenhum histórico encontrado para essa corrida.")
        return

    print("\n========== HISTÓRICO DA CORRIDA ==========")

    for registro in historico:
        print(f"ID do registro: {registro[0]}")
        print(f"ID da corrida: {registro[1]}")
        print(f"Status anterior: {registro[2]}")
        print(f"Novo status: {registro[3]}")
        print(f"Data da alteração: {registro[4]}")
        print("-----------------------------------------")


def arrecadacao_periodo():
    conexao = conectar()
    cursor = conexao.cursor()

    data_inicio = input("Digite a data inicial (AAAA-MM-DD): ")
    data_fim = input("Digite a data final (AAAA-MM-DD): ")

    cursor.execute("""
        SELECT
            COUNT(*) AS quantidade_pagamentos,
            COALESCE(SUM(valor), 0)
        FROM pagamentos
        WHERE status = 'Pago'
          AND DATE(data_pagamento) BETWEEN DATE(?) AND DATE(?)
    """, (data_inicio, data_fim))

    resultado = cursor.fetchone()

    conexao.close()

    print("\n========== ARRECADAÇÃO DO PERÍODO ==========")
    print(f"Data inicial: {data_inicio}")
    print(f"Data final: {data_fim}")
    print(f"Quantidade de pagamentos: {resultado[0]}")
    print(f"Arrecadação: R$ {resultado[1]:.2f}")


def media_avaliacao_motoristas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            motoristas.id,
            motoristas.nome,
            COUNT(avaliacoes.id) AS quantidade_avaliacoes,
            ROUND(AVG(avaliacoes.nota), 2) AS media
        FROM motoristas
        INNER JOIN corridas
            ON motoristas.id = corridas.id_motorista
        INNER JOIN avaliacoes
            ON corridas.id = avaliacoes.id_corrida
        GROUP BY motoristas.id, motoristas.nome
        ORDER BY media DESC
    """)

    # Lista de Tuplas
    motoristas = cursor.fetchall()

    conexao.close()

    if not motoristas:
        print("\nNenhuma avaliação encontrada.")
        return

    print("\n========== MÉDIA DE AVALIAÇÃO DOS MOTORISTAS ==========")

    for motorista in motoristas:
        print(f"ID: {motorista[0]}")
        print(f"Nome: {motorista[1]}")
        print(f"Quantidade de avaliações: {motorista[2]}")
        print(f"Média: {motorista[3]:.2f}")
        print("------------------------------------------------------")


def media_geral_motoristas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS quantidade_avaliacoes,
            ROUND(AVG(nota), 2) AS media_geral
        FROM avaliacoes
    """)

    resultado = cursor.fetchone()

    conexao.close()

    if resultado[0] == 0:
        print("\nNenhuma avaliação encontrada.")
        return

    print("\n========== MÉDIA GERAL DOS MOTORISTAS ==========")
    print(f"Quantidade de avaliações: {resultado[0]}")
    print(f"Média geral: {resultado[1]:.2f}")
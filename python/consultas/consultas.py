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
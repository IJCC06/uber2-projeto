from banco.conexao import conectar

# Registrar Histórico (Sistema):
def registrar_historico(id_corrida, status_anterior, novo_status):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO historico_corridas (
            id_corrida,
            status_anterior,
            novo_status
        )
        VALUES (?, ?, ?)
    """, (
        id_corrida,
        status_anterior,
        novo_status
    ))

    conexao.commit()
    conexao.close()


# Listar Histórico de Corrida (ADM)
def listar_historico_corrida():
    conexao = conectar()
    cursor = conexao.cursor()

    id_corrida = int(input("Digite o ID da corrida: "))

    cursor.execute("""
        SELECT
            id,
            status_anterior,
            novo_status,
            data_alteracao
        FROM historico_corridas
        WHERE id_corrida = ?
        ORDER BY id
    """, (id_corrida,))

    historico = cursor.fetchall()

    conexao.close()

    if not historico:
        print("\nNenhum histórico encontrado para essa corrida.")
        return

    print("\n========== HISTÓRICO DA CORRIDA ==========")

    for item in historico:
        print(f"ID do registro: {item[0]}")
        print(f"Status anterior: {item[1]}")
        print(f"Novo status: {item[2]}")
        print(f"Data da alteração: {item[3]}")
        print("------------------------------------------")


# Listar Histórico Corridas (Motorista)
def listar_historico_motorista(id_motorista):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            historico_corridas.id,
            historico_corridas.id_corrida,
            historico_corridas.status_anterior,
            historico_corridas.novo_status,
            historico_corridas.data_alteracao
        FROM historico_corridas
        INNER JOIN corridas
            ON historico_corridas.id_corrida = corridas.id
        WHERE corridas.id_motorista = ?
        ORDER BY historico_corridas.id DESC
    """, (id_motorista,))

    historico = cursor.fetchall()

    conexao.close()

    if not historico:
        print("\nNenhum histórico encontrado.")
        return

    print("\n========== MEU HISTÓRICO ==========")

    for item in historico:
        print(f"ID do registro: {item[0]}")
        print(f"ID da corrida: {item[1]}")
        print(f"Status anterior: {item[2]}")
        print(f"Novo status: {item[3]}")
        print(f"Data da alteração: {item[4]}")
        print("-----------------------------------")


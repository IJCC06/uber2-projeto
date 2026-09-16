from banco.conexao import conectar

# Cadastrar Veículos
def cadastrar_veiculo(id_motorista):
    conexao = conectar()
    cursor = conexao.cursor()

    modelo = input("Insira o modelo: ")
    marca = input("Insira a marca: ")
    placa = input("Insira a placa: ")
    ano = int(input("Insira o ano: "))
    cor = input("Insira a cor: ")

    cursor.execute("""
        INSERT INTO veiculos (
            id_motorista,
            modelo,
            marca,
            placa,
            ano,
            cor
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        id_motorista,
        modelo,
        marca,
        placa,
        ano,
        cor
    ))

    conexao.commit()
    conexao.close()

    print("Veículo cadastrado com sucesso!")


# Listar Veículos (Motorista)
def listar_veiculos(id_motorista):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, modelo, marca, placa, ano, cor
        FROM veiculos
        WHERE id_motorista = ?
        ORDER BY id
    """, (id_motorista,))

    veiculos = cursor.fetchall()

    conexao.close()

    if not veiculos:
        print("\nVocê não possui veículos cadastrados.")
        return

    print("\n========== MEUS VEÍCULOS ==========")

    for veiculo in veiculos:
        print(f"ID: {veiculo[0]}")
        print(f"Modelo: {veiculo[1]}")
        print(f"Marca: {veiculo[2]}")
        print(f"Placa: {veiculo[3]}")
        print(f"Ano: {veiculo[4]}")
        print(f"Cor: {veiculo[5]}")
        print("-----------------------------------")


# Editar Veículo (Motorista)
def editar_veiculo(id_motorista):
    conexao = conectar()
    cursor = conexao.cursor()

    id_veiculo = int(input("Digite o ID do veículo que deseja editar: "))

    cursor.execute("""
        SELECT modelo, marca, placa, ano, cor
        FROM veiculos
        WHERE id = ? AND id_motorista = ?
    """, (id_veiculo, id_motorista))

    veiculo = cursor.fetchone()

    if veiculo is None:
        print("Veículo não encontrado ou não pertence a você.")
        conexao.close()
        return

    print("\n--- EDITAR VEÍCULO ---")
    print("Deixe vazio para manter o valor atual.\n")

    modelo = input(f"Modelo [{veiculo[0]}]: ")
    marca = input(f"Marca [{veiculo[1]}]: ")
    placa = input(f"Placa [{veiculo[2]}]: ")
    ano = input(f"Ano [{veiculo[3]}]: ")
    cor = input(f"Cor [{veiculo[4]}]: ")

    if modelo == "":
        modelo = veiculo[0]

    if marca == "":
        marca = veiculo[1]

    if placa == "":
        placa = veiculo[2]

    if ano == "":
        ano = veiculo[3]
    else:
        ano = int(ano)

    if cor == "":
        cor = veiculo[4]

    cursor.execute("""
        UPDATE veiculos
        SET modelo = ?,
            marca = ?,
            placa = ?,
            ano = ?,
            cor = ?
        WHERE id = ? AND id_motorista = ?
    """, (
        modelo,
        marca,
        placa,
        ano,
        cor,
        id_veiculo,
        id_motorista
    ))

    conexao.commit()
    conexao.close()

    print("Veículo atualizado com sucesso!")


# Excluir Veículos
def excluir_veiculo(id_motorista):
    conexao = conectar()
    cursor = conexao.cursor()

    id_veiculo = int(input("Digite o ID do veículo que deseja excluir: "))

    cursor.execute("""
        SELECT modelo, marca, placa
        FROM veiculos
        WHERE id = ? AND id_motorista = ?
    """, (id_veiculo, id_motorista))

    veiculo = cursor.fetchone()

    if veiculo is None:
        print("Veículo não encontrado ou não pertence a você.")
        conexao.close()
        return

    print("\n--- VEÍCULO SELECIONADO ---")
    print(f"Modelo: {veiculo[0]}")
    print(f"Marca: {veiculo[1]}")
    print(f"Placa: {veiculo[2]}")

    confirmacao = input(
        "\nTem certeza que deseja excluir este veículo? (S/N): "
    )

    if confirmacao.upper() != "S":
        print("Exclusão cancelada.")
        conexao.close()
        return

    cursor.execute("""
        DELETE FROM veiculos
        WHERE id = ? AND id_motorista = ?
    """, (id_veiculo, id_motorista))

    conexao.commit()
    conexao.close()

    print("Veículo excluído com sucesso!")


# Listar todos os Veículos (ADM)
def listar_todos_veiculos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            veiculos.id,
            veiculos.modelo,
            veiculos.marca,
            veiculos.placa,
            veiculos.ano,
            veiculos.cor,
            motoristas.nome
        FROM veiculos
        INNER JOIN motoristas
            ON veiculos.id_motorista = motoristas.id
        ORDER BY veiculos.id
    """)

    veiculos = cursor.fetchall()

    conexao.close()

    if not veiculos:
        print("\nNenhum veículo cadastrado.")
        return

    print("\n========== TODOS OS VEÍCULOS ==========")

    for veiculo in veiculos:
        print(f"ID: {veiculo[0]}")
        print(f"Modelo: {veiculo[1]}")
        print(f"Marca: {veiculo[2]}")
        print(f"Placa: {veiculo[3]}")
        print(f"Ano: {veiculo[4]}")
        print(f"Cor: {veiculo[5]}")
        print(f"Motorista: {veiculo[6]}")
        print("---------------------------------------")


# Editar Veículo (ADM)
def editar_veiculo_admin():
    conexao = conectar()
    cursor = conexao.cursor()

    id_veiculo = int(input("Digite o ID do veículo que deseja editar: "))

    cursor.execute("""
        SELECT modelo, marca, placa, ano, cor
        FROM veiculos
        WHERE id = ?
    """, (id_veiculo,))

    veiculo = cursor.fetchone()

    if veiculo is None:
        print("Veículo não encontrado.")
        conexao.close()
        return

    print("\n--- EDITAR VEÍCULO ---")
    print("Deixe vazio para manter o valor atual.\n")

    modelo = input(f"Modelo [{veiculo[0]}]: ")
    marca = input(f"Marca [{veiculo[1]}]: ")
    placa = input(f"Placa [{veiculo[2]}]: ")
    ano = input(f"Ano [{veiculo[3]}]: ")
    cor = input(f"Cor [{veiculo[4]}]: ")

    if modelo == "":
        modelo = veiculo[0]

    if marca == "":
        marca = veiculo[1]

    if placa == "":
        placa = veiculo[2]

    if ano == "":
        ano = veiculo[3]
    else:
        ano = int(ano)

    if cor == "":
        cor = veiculo[4]

    cursor.execute("""
        UPDATE veiculos
        SET modelo = ?,
            marca = ?,
            placa = ?,
            ano = ?,
            cor = ?
        WHERE id = ?
    """, (
        modelo,
        marca,
        placa,
        ano,
        cor,
        id_veiculo
    ))

    conexao.commit()
    conexao.close()

    print("Veículo atualizado com sucesso!")


# Excluir Veículo (ADM)
def excluir_veiculo_admin():
    conexao = conectar()
    cursor = conexao.cursor()

    id_veiculo = int(input("Digite o ID do veículo que deseja excluir: "))

    cursor.execute("""
        SELECT modelo, marca, placa
        FROM veiculos
        WHERE id = ?
    """, (id_veiculo,))

    veiculo = cursor.fetchone()

    if veiculo is None:
        print("Veículo não encontrado.")
        conexao.close()
        return

    print("\n--- VEÍCULO SELECIONADO ---")
    print(f"Modelo: {veiculo[0]}")
    print(f"Marca: {veiculo[1]}")
    print(f"Placa: {veiculo[2]}")

    confirmacao = input(
        "Tem certeza que deseja excluir este veículo? (S/N): "
    )

    if confirmacao.upper() != "S":
        print("Exclusão cancelada.")
        conexao.close()
        return

    cursor.execute("""
        DELETE FROM veiculos
        WHERE id = ?
    """, (id_veiculo,))

    conexao.commit()
    conexao.close()

    print("Veículo excluído com sucesso!")
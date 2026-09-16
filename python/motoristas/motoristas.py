from banco.conexao import conectar

# Cadastro de Motorista
def cadastrar_motorista():
    conexao = conectar()
    cursor = conexao.cursor()

    nome = input("Digite o nome: ")
    cpf = input("Digite o CPF: ")
    telefone = input("Digite o telefone: ")
    cnh = input("Digite a CNH: ")

    cursor.execute("""
        INSERT INTO motoristas (nome, cpf, telefone, cnh)
        VALUES
        (?, ?, ?, ?)
    """, (nome, cpf, telefone, cnh))

    conexao.commit()
    conexao.close()
    print("Motorista cadastrado com sucesso!")


# Edição de Motorista
def editar_motorista(id_motorista):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome, cpf, telefone, cnh
        FROM motoristas
        WHERE id = ?
    """, (id_motorista,))

    motorista = cursor.fetchone()

    if motorista is None:
        print("Motorista não encontrado!")
        conexao.close()
        return

    print("\n--- EDITAR DADOS ---")
    print("Deixe vazio para manter o valor atual.\n")

    nome = input(f"Nome [{motorista[0]}]: ")
    cpf = input(f"CPF [{motorista[1]}]: ")
    telefone = input(f"Telefone [{motorista[2]}]: ")
    cnh = input(f"CNH [{motorista[3]}]: ")

    if nome == "":
        nome = motorista[0]
    if cpf == "":
        cpf = motorista[1]
    if telefone == "":
        telefone = motorista[2]
    if cnh == "":
        cnh = motorista[3]

    cursor.execute("""
        UPDATE motoristas
        SET nome = ?,
            cpf = ?,
            telefone = ?,
            cnh = ?
        WHERE id = ?
    """, (nome, cpf, telefone, cnh, id_motorista))

    conexao.commit()
    conexao.close()
    print("Dados atualizados com sucesso!")


# Listar Motoristas (ADM)
def listar_motoristas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, cpf, telefone, cnh, status
        FROM motoristas
        ORDER BY id
    """)

    motoristas = cursor.fetchall()

    conexao.close()

    if not motoristas:
        print("\nNenhum motorista cadastrado.")
        return

    print("\n========== MOTORISTAS ==========")

    for motorista in motoristas:
        print(f"ID: {motorista[0]}")
        print(f"Nome: {motorista[1]}")
        print(f"CPF: {motorista[2]}")
        print(f"Telefone: {motorista[3]}")
        print(f"CNH: {motorista[4]}")
        print(f"Status: {motorista[5]}")
        print("-------------------------------")


# Alterar Status do Motorista (ADM)
def alterar_status_motorista():
    conexao = conectar()
    cursor = conexao.cursor()

    id_motorista = int(input("Digite o ID do motorista: "))

    cursor.execute("""
        SELECT nome, status
        FROM motoristas
        WHERE id = ?
    """, (id_motorista,))

    motorista = cursor.fetchone()

    if motorista is None:
        print("Motorista não encontrado!")
        conexao.close()
        return

    print(f"\nMotorista: {motorista[0]}")
    print(f"Status atual: {motorista[1]}")

    novo_status = input(
        "Digite o novo status (Ativo/Inativo): "
    ).strip().capitalize()

    if novo_status not in ("Ativo", "Inativo"):
        print("Status inválido!")
        print("Use apenas Ativo ou Inativo.")
        conexao.close()
        return

    cursor.execute("""
        UPDATE motoristas
        SET status = ?
        WHERE id = ?
    """, (novo_status, id_motorista))

    conexao.commit()
    conexao.close()

    print("Status do motorista atualizado com sucesso!")


# Editar Motorista (ADM)
def editar_motorista_admin():
    conexao = conectar()
    cursor = conexao.cursor()

    id_motorista = int(input("Digite o ID do motorista que deseja editar: "))

    cursor.execute("""
        SELECT nome, cpf, telefone, cnh
        FROM motoristas
        WHERE id = ?
    """, (id_motorista,))

    motorista = cursor.fetchone()

    if motorista is None:
        print("Motorista não encontrado!")
        conexao.close()
        return

    print("\n--- EDITAR MOTORISTA ---")
    print(f"Nome atual: {motorista[0]}")
    print(f"CPF atual: {motorista[1]}")
    print(f"Telefone atual: {motorista[2]}")
    print(f"CNH atual: {motorista[3]}")
    print("Deixe vazio para manter o valor atual.\n")

    nome = input(f"Novo nome [{motorista[0]}]: ")
    cpf = input(f"Novo CPF [{motorista[1]}]: ")
    telefone = input(f"Novo telefone [{motorista[2]}]: ")
    cnh = input(f"Nova CNH [{motorista[3]}]: ")

    if nome == "":
        nome = motorista[0]

    if cpf == "":
        cpf = motorista[1]

    if telefone == "":
        telefone = motorista[2]

    if cnh == "":
        cnh = motorista[3]

    cursor.execute("""
        UPDATE motoristas
        SET nome = ?,
            cpf = ?,
            telefone = ?,
            cnh = ?
        WHERE id = ?
    """, (nome, cpf, telefone, cnh, id_motorista))

    conexao.commit()
    conexao.close()

    print("Motorista atualizado com sucesso!")


# Excluir Motorista (ADM)
def excluir_motorista_admin():
    conexao = conectar()
    cursor = conexao.cursor()

    id_motorista = int(input("Digite o ID do motorista que deseja excluir: "))

    cursor.execute("""
        SELECT nome
        FROM motoristas
        WHERE id = ?
    """, (id_motorista,))

    motorista = cursor.fetchone()

    if motorista is None:
        print("Motorista não encontrado!")
        conexao.close()
        return

    print(f"\nMotorista selecionado: {motorista[0]}")

    confirmacao = input(
        "Tem certeza que deseja excluir este motorista? (S/N): "
    )

    if confirmacao.upper() != "S":
        print("Exclusão cancelada.")
        conexao.close()
        return

    cursor.execute("""
        SELECT COUNT(*)
        FROM corridas
        WHERE id_motorista = ?
    """, (id_motorista,))

    quantidade_corridas = cursor.fetchone()[0]

    if quantidade_corridas > 0:
        print("Não é possível excluir este motorista.")
        print("Ele possui corridas cadastradas.")
        conexao.close()
        return

    cursor.execute("""
        DELETE FROM motoristas
        WHERE id = ?
    """, (id_motorista,))

    conexao.commit()
    conexao.close()

    print("Motorista excluído com sucesso!")
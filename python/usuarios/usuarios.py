from banco.conexao import conectar

# Cadastrar Usuário
def cadastrar_usuario():
    conexao = conectar()
    cursor = conexao.cursor()

    nome = input("Insira o nome: ")
    email = input("Insira o e-mail: ")
    telefone = input("Insira o telefone: ")
    senha = input("Insira a senha: ")

    cursor.execute("""
        INSERT INTO usuarios (nome, email, telefone, senha)
        VALUES (?, ?, ?, ?)
    """, (nome, email, telefone, senha))

    conexao.commit()
    conexao.close()

    print("Usuário cadastrado com sucesso!")


# Editar Usuário
def editar_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome, email, telefone, senha
        FROM usuarios
        WHERE id = ?
    """, (id_usuario,))

    usuario = cursor.fetchone()

    if usuario is None:
        print("Usuário não encontrado.")
        conexao.close()
        return

    print("\n--- EDITAR DADOS ---")
    print("Deixe vazio para manter o valor atual.\n")

    nome = input(f"Nome [{usuario[0]}]: ")
    email = input(f"E-mail [{usuario[1]}]: ")
    telefone = input(f"Telefone [{usuario[2]}]: ")
    senha = input("Nova senha [não alterada]: ")

    if nome == "":
        nome = usuario[0]

    if email == "":
        email = usuario[1]

    if telefone == "":
        telefone = usuario[2]

    if senha == "":
        senha = usuario[3]

    cursor.execute("""
        UPDATE usuarios
        SET nome = ?,
            email = ?,
            telefone = ?,
            senha = ?
        WHERE id = ?
    """, (nome, email, telefone, senha, id_usuario))

    conexao.commit()
    conexao.close()

    print("Dados atualizados com sucesso!")


# Excluir Usuário
def excluir_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome
        FROM usuarios
        WHERE id = ?
    """, (id_usuario,))

    usuario = cursor.fetchone()

    if usuario is None:
        print("Usuário não encontrado.")
        conexao.close()
        return

    print(f"\nUsuário: {usuario[0]}")

    confirmacao = input(
        "Tem certeza que deseja excluir sua conta? (S/N): "
    )

    if confirmacao.upper() != "S":
        print("Exclusão cancelada.")
        conexao.close()
        return

    cursor.execute("""
        SELECT COUNT(*)
        FROM corridas
        WHERE id_usuario = ?
    """, (id_usuario,))

    quantidade_corridas = cursor.fetchone()[0]

    if quantidade_corridas > 0:
        print("Não é possível excluir a conta.")
        print("Este usuário possui corridas cadastradas.")
        conexao.close()
        return

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id = ?
    """, (id_usuario,))

    conexao.commit()
    conexao.close()

    print("Conta excluída com sucesso!")


# Listar Usuários (ADM)
def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, email, telefone, data_cadastro
        FROM usuarios
        ORDER BY id
    """)

    usuarios = cursor.fetchall()

    conexao.close()

    if not usuarios:
        print("\nNenhum usuário cadastrado.")
        return

    print("\n========== USUÁRIOS ==========")

    for usuario in usuarios:
        print(f"ID: {usuario[0]}")
        print(f"Nome: {usuario[1]}")
        print(f"E-mail: {usuario[2]}")
        print(f"Telefone: {usuario[3]}")
        print(f"Data de cadastro: {usuario[4]}")
        print("------------------------------")


# Editar Usuário (ADM)
def editar_usuario_admin():
    conexao = conectar()
    cursor = conexao.cursor()

    id_usuario = int(input("Digite o ID do usuário que deseja editar: "))

    cursor.execute("""
        SELECT nome, email, telefone, senha
        FROM usuarios
        WHERE id = ?
    """, (id_usuario,))

    usuario = cursor.fetchone()

    if usuario is None:
        print("Usuário não encontrado.")
        conexao.close()
        return

    print("\n--- EDITAR USUÁRIO ---")
    print(f"Nome atual: {usuario[0]}")
    print(f"E-mail atual: {usuario[1]}")
    print(f"Telefone atual: {usuario[2]}")
    print()

    nome = input(f"Novo nome [{usuario[0]}]: ")
    email = input(f"Novo e-mail [{usuario[1]}]: ")
    telefone = input(f"Novo telefone [{usuario[2]}]: ")
    senha = input("Nova senha [não alterada]: ")

    if nome == "":
        nome = usuario[0]

    if email == "":
        email = usuario[1]

    if telefone == "":
        telefone = usuario[2]

    if senha == "":
        senha = usuario[3]

    cursor.execute("""
        UPDATE usuarios
        SET nome = ?,
            email = ?,
            telefone = ?,
            senha = ?
        WHERE id = ?
    """, (nome, email, telefone, senha, id_usuario))

    conexao.commit()
    conexao.close()

    print("Usuário atualizado com sucesso!")


# Excluir Usuário (ADM)
def excluir_usuario_admin():
    conexao = conectar()
    cursor = conexao.cursor()

    id_usuario = int(input("Digite o ID do usuário que deseja excluir: "))

    cursor.execute("""
        SELECT nome
        FROM usuarios
        WHERE id = ?
    """, (id_usuario,))

    usuario = cursor.fetchone()

    if usuario is None:
        print("Usuário não encontrado.")
        conexao.close()
        return

    print(f"\nUsuário selecionado: {usuario[0]}")

    confirmacao = input(
        "Tem certeza que deseja excluir este usuário? (S/N): "
    )

    if confirmacao.upper() != "S":
        print("Exclusão cancelada.")
        conexao.close()
        return

    cursor.execute("""
        SELECT COUNT(*)
        FROM corridas
        WHERE id_usuario = ?
    """, (id_usuario,))

    quantidade_corridas = cursor.fetchone()[0]

    if quantidade_corridas > 0:
        print("Não é possível excluir este usuário.")
        print("Ele possui corridas cadastradas.")
        conexao.close()
        return

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id = ?
    """, (id_usuario,))

    conexao.commit()
    conexao.close()

    print("Usuário excluído com sucesso!")
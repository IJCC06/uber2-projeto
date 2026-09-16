from banco.conexao import conectar

# Cadastrar Avaliação
def cadastrar_avaliacao(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    id_corrida = int(
        input("Digite o ID da corrida que deseja avaliar: ")
    )

    cursor.execute("""
        SELECT id_motorista, status
        FROM corridas
        WHERE id = ?
          AND id_usuario = ?
    """, (id_corrida, id_usuario))

    corrida = cursor.fetchone()

    if corrida is None:
        print("Corrida não encontrada ou não pertence a você.")
        conexao.close()
        return

    id_motorista = corrida[0]
    status_corrida = corrida[1]

    if status_corrida != "Finalizada":
        print("Só é possível avaliar uma corrida finalizada.")
        conexao.close()
        return

    if id_motorista is None:
        print("Essa corrida não possui motorista.")
        conexao.close()
        return

    cursor.execute("""
        SELECT id
        FROM avaliacoes
        WHERE id_corrida = ?
    """, (id_corrida,))

    avaliacao = cursor.fetchone()

    if avaliacao is not None:
        print("Essa corrida já foi avaliada.")
        conexao.close()
        return

    nota = int(input("Digite a nota de 1 a 5: "))

    if nota < 1 or nota > 5:
        print("A nota deve estar entre 1 e 5.")
        conexao.close()
        return

    comentario = input("Digite um comentário (opcional): ")

    cursor.execute("""
        INSERT INTO avaliacoes (
            id_corrida,
            nota,
            comentario
        )
        VALUES (?, ?, ?)
    """, (
        id_corrida,
        nota,
        comentario
    ))

    conexao.commit()
    conexao.close()

    print("Avaliação cadastrada com sucesso!")


# Listar Avaliações (ADM)
def listar_avaliacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            avaliacoes.id,
            avaliacoes.id_corrida,
            usuarios.nome,
            motoristas.nome,
            avaliacoes.nota,
            avaliacoes.comentario,
            avaliacoes.data_avaliacao
        FROM avaliacoes
        INNER JOIN corridas
            ON avaliacoes.id_corrida = corridas.id
        INNER JOIN usuarios
            ON corridas.id_usuario = usuarios.id
        INNER JOIN motoristas
            ON corridas.id_motorista = motoristas.id
        ORDER BY avaliacoes.id
    """)

    avaliacoes = cursor.fetchall()

    conexao.close()

    if not avaliacoes:
        print("\nNenhuma avaliação cadastrada.")
        return

    print("\n========== TODAS AS AVALIAÇÕES ==========")

    for avaliacao in avaliacoes:
        print(f"ID da avaliação: {avaliacao[0]}")
        print(f"ID da corrida: {avaliacao[1]}")
        print(f"Usuário: {avaliacao[2]}")
        print(f"Motorista: {avaliacao[3]}")
        print(f"Nota: {avaliacao[4]}")
        print(f"Comentário: {avaliacao[5]}")
        print(f"Data: {avaliacao[6]}")
        print("-----------------------------------------")


# Editar Avaliação (ADM)
def editar_avaliacao():
    conexao = conectar()
    cursor = conexao.cursor()

    id_avaliacao = int(
        input("Digite o ID da avaliação que deseja editar: ")
    )

    cursor.execute("""
        SELECT nota, comentario
        FROM avaliacoes
        WHERE id = ?
    """, (id_avaliacao,))

    avaliacao = cursor.fetchone()

    if avaliacao is None:
        print("Avaliação não encontrada.")
        conexao.close()
        return

    print("\n--- EDITAR AVALIAÇÃO ---")
    print("Deixe vazio para manter o valor atual.\n")

    nota = input(f"Nota [{avaliacao[0]}]: ")

    if nota == "":
        nova_nota = avaliacao[0]
    else:
        nova_nota = int(nota)

        if nova_nota < 1 or nova_nota > 5:
            print("A nota deve estar entre 1 e 5.")
            conexao.close()
            return

    comentario = input(
        f"Comentário [{avaliacao[1]}]: "
    )

    if comentario == "":
        novo_comentario = avaliacao[1]
    else:
        novo_comentario = comentario

    cursor.execute("""
        UPDATE avaliacoes
        SET nota = ?,
            comentario = ?
        WHERE id = ?
    """, (
        nova_nota,
        novo_comentario,
        id_avaliacao
    ))

    conexao.commit()
    conexao.close()

    print("Avaliação atualizada com sucesso!")


# Excluir Avaliação (ADM)
def excluir_avaliacao():
    conexao = conectar()
    cursor = conexao.cursor()

    id_avaliacao = int(
        input("Digite o ID da avaliação que deseja excluir: ")
    )

    cursor.execute("""
        SELECT nota, comentario
        FROM avaliacoes
        WHERE id = ?
    """, (id_avaliacao,))

    avaliacao = cursor.fetchone()

    if avaliacao is None:
        print("Avaliação não encontrada.")
        conexao.close()
        return

    print("\n--- AVALIAÇÃO SELECIONADA ---")
    print(f"Nota: {avaliacao[0]}")
    print(f"Comentário: {avaliacao[1]}")

    confirmacao = input(
        "Tem certeza que deseja excluir esta avaliação? (S/N): "
    )

    if confirmacao.upper() != "S":
        print("Exclusão cancelada.")
        conexao.close()
        return

    cursor.execute("""
        DELETE FROM avaliacoes
        WHERE id = ?
    """, (id_avaliacao,))

    conexao.commit()
    conexao.close()

    print("Avaliação excluída com sucesso!")
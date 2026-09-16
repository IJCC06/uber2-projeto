from banco.conexao import conectar

from usuarios.usuarios import (
    cadastrar_usuario,
    editar_usuario,
    excluir_usuario,
    listar_usuarios,
    editar_usuario_admin,
    excluir_usuario_admin
)

from motoristas.motoristas import (
    cadastrar_motorista,
    editar_motorista,
    listar_motoristas,
    alterar_status_motorista,
    editar_motorista_admin,
    excluir_motorista_admin
)

from veiculos.veiculos import (
    cadastrar_veiculo,
    listar_veiculos,
    editar_veiculo,
    excluir_veiculo,
    listar_todos_veiculos,
    editar_veiculo_admin,
    excluir_veiculo_admin
)

from corridas.corridas import (
    cadastrar_corrida,
    listar_corridas_usuario,
    listar_corridas_disponiveis,
    aceitar_corrida,
    atualizar_status_corrida,
    listar_todas_corridas,
    editar_corrida,
    excluir_corrida
)

from pagamentos.pagamentos import (
    cadastrar_pagamento,
    listar_pagamentos_usuario,
    listar_pagamentos,
    editar_pagamento,
    excluir_pagamento
)

from avaliacoes.avaliacoes import (
    cadastrar_avaliacao,
    listar_avaliacoes,
    editar_avaliacao,
    excluir_avaliacao
)

from historico.historico import (
    listar_historico_corrida,
    listar_historico_motorista
)

from consultas.consultas import (
    cinco_corridas_mais_caras,
    motorista_mais_corridas,
    forma_pagamento_mais_utilizada,
    usuarios_mais_corridas,
    motoristas_disponiveis,
    historico_determinada_corrida,
    arrecadacao_periodo,
    media_avaliacao_motoristas,
    media_geral_motoristas
)

# SENHA DO ADMIN
SENHA_ADMIN = "OInimigoEoTransito"


def menu_usuario(id_usuario):
    while True:
        print("\n========== MENU DO USUÁRIO ==========")
        print("1 - Solicitar corrida")
        print("2 - Minhas corridas")
        print("3 - Cadastrar pagamento")
        print("4 - Meus pagamentos")
        print("5 - Avaliar corrida")
        print("6 - Editar meus dados")
        print("7 - Excluir minha conta")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_corrida(id_usuario)

        elif opcao == "2":
            listar_corridas_usuario(id_usuario)

        elif opcao == "3":
            cadastrar_pagamento(id_usuario)

        elif opcao == "4":
            listar_pagamentos_usuario(id_usuario)

        elif opcao == "5":
            cadastrar_avaliacao(id_usuario)

        elif opcao == "6":
            editar_usuario(id_usuario)

        elif opcao == "7":
            excluir_usuario(id_usuario)
            break

        elif opcao == "0":
            print("\nSaindo...")
            break

        else:
            print("\nOpção inválida.")


def menu_motorista(id_motorista):
    while True:
        print("\n========== MENU DO MOTORISTA ==========")
        print("1 - Visualizar corridas disponíveis")
        print("2 - Aceitar corrida")
        print("3 - Atualizar status da corrida")
        print("4 - Cadastrar veículo")
        print("5 - Meus veículos")
        print("6 - Editar veículo")
        print("7 - Excluir veículo")
        print("8 - Meu histórico")
        print("9 - Editar meus dados")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_corridas_disponiveis()

        elif opcao == "2":
            aceitar_corrida(id_motorista)

        elif opcao == "3":
            atualizar_status_corrida(id_motorista)

        elif opcao == "4":
            cadastrar_veiculo(id_motorista)

        elif opcao == "5":
            listar_veiculos(id_motorista)

        elif opcao == "6":
            editar_veiculo(id_motorista)

        elif opcao == "7":
            excluir_veiculo(id_motorista)

        elif opcao == "8":
            listar_historico_motorista(id_motorista)

        elif opcao == "9":
            editar_motorista(id_motorista)

        elif opcao == "0":
            print("\nSaindo...")
            break

        else:
            print("\nOpção inválida.")


def menu_admin():
    while True:
        print("\n========== MENU DO ADMINISTRADOR ==========")
        print("1 - Gerenciar usuários")
        print("2 - Gerenciar motoristas")
        print("3 - Gerenciar veículos")
        print("4 - Gerenciar corridas")
        print("5 - Gerenciar pagamentos")
        print("6 - Gerenciar avaliações")
        print("7 - Consultas e relatórios")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_admin_usuarios()

        elif opcao == "2":
            menu_admin_motoristas()

        elif opcao == "3":
            menu_admin_veiculos()

        elif opcao == "4":
            menu_admin_corridas()

        elif opcao == "5":
            menu_admin_pagamentos()

        elif opcao == "6":
            menu_admin_avaliacoes()

        elif opcao == "7":
            menu_consultas()

        elif opcao == "0":
            print("\nSaindo...")
            break

        else:
            print("\nOpção inválida.")


# SubMenus do Admin
def menu_admin_usuarios():
    while True:
        print("\n========== GERENCIAR USUÁRIOS ==========")
        print("1 - Listar usuários")
        print("2 - Editar usuário")
        print("3 - Excluir usuário")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_usuarios()

        elif opcao == "2":
            editar_usuario_admin()

        elif opcao == "3":
            excluir_usuario_admin()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


def menu_admin_motoristas():
    while True:
        print("\n========== GERENCIAR MOTORISTAS ==========")
        print("1 - Cadastrar motorista")
        print("2 - Listar motoristas")
        print("3 - Editar motorista")
        print("4 - Alterar status do motorista")
        print("5 - Excluir motorista")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_motorista()

        elif opcao == "2":
            listar_motoristas()

        elif opcao == "3":
            editar_motorista_admin()

        elif opcao == "4":
            alterar_status_motorista()

        elif opcao == "5":
            excluir_motorista_admin()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


def menu_admin_veiculos():
    while True:
        print("\n========== GERENCIAR VEÍCULOS ==========")
        print("1 - Listar veículos")
        print("2 - Editar veículo")
        print("3 - Excluir veículo")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_todos_veiculos()

        elif opcao == "2":
            editar_veiculo_admin()

        elif opcao == "3":
            excluir_veiculo_admin()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


def menu_admin_corridas():
    while True:
        print("\n========== GERENCIAR CORRIDAS ==========")
        print("1 - Listar corridas")
        print("2 - Editar corrida")
        print("3 - Excluir corrida")
        print("4 - Consultar histórico de uma corrida")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_todas_corridas()

        elif opcao == "2":
            editar_corrida()

        elif opcao == "3":
            excluir_corrida()

        elif opcao == "4":
            listar_historico_corrida()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


def menu_admin_pagamentos():
    while True:
        print("\n========== GERENCIAR PAGAMENTOS ==========")
        print("1 - Listar pagamentos")
        print("2 - Editar pagamento")
        print("3 - Excluir pagamento")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_pagamentos()

        elif opcao == "2":
            editar_pagamento()

        elif opcao == "3":
            excluir_pagamento()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


def menu_admin_avaliacoes():
    while True:
        print("\n========== GERENCIAR AVALIAÇÕES ==========")
        print("1 - Listar avaliações")
        print("2 - Editar avaliação")
        print("3 - Excluir avaliação")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_avaliacoes()

        elif opcao == "2":
            editar_avaliacao()

        elif opcao == "3":
            excluir_avaliacao()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


def menu_consultas():
    while True:
        print("\n========== CONSULTAS E RELATÓRIOS ==========")
        print("1 - 5 corridas mais caras")
        print("2 - Motorista com mais corridas")
        print("3 - Forma de pagamento mais utilizada")
        print("4 - Usuários com mais corridas")
        print("5 - Motoristas disponíveis")
        print("6 - Histórico de determinada corrida")
        print("7 - Arrecadação por período")
        print("8 - Média de avaliação dos motoristas")
        print("9 - Média geral dos motoristas")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cinco_corridas_mais_caras()

        elif opcao == "2":
            motorista_mais_corridas()

        elif opcao == "3":
            forma_pagamento_mais_utilizada()

        elif opcao == "4":
            usuarios_mais_corridas()

        elif opcao == "5":
            motoristas_disponiveis()

        elif opcao == "6":
            historico_determinada_corrida()

        elif opcao == "7":
            arrecadacao_periodo()

        elif opcao == "8":
            media_avaliacao_motoristas()

        elif opcao == "9":
            media_geral_motoristas()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


# Login
def login():
    print("\n========== LOGIN ==========")
    print("1 - Usuário")
    print("2 - Motorista")
    print("3 - Administrador")
    print("0 - Voltar")

    tipo = input("Escolha uma opção: ")

    if tipo == "1":
        email = input("E-mail: ")
        senha = input("Senha: ")

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome
            FROM usuarios
            WHERE email = ?
              AND senha = ?
        """, (email, senha))

        usuario = cursor.fetchone()

        conexao.close()

        if not usuario:
            print("\nE-mail ou senha incorretos.")
            return

        print(f"\nBem-vindo(a), {usuario[1]}!")

        menu_usuario(usuario[0])


    elif tipo == "2":
        cpf = input("CPF: ")

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome
            FROM motoristas
            WHERE cpf = ?
              AND status = 'Ativo'
        """, (cpf,))

        motorista = cursor.fetchone()

        conexao.close()

        if not motorista:
            print("\nMotorista não encontrado ou está inativo.")
            return

        print(f"\nBem-vindo(a), {motorista[1]}!")

        menu_motorista(motorista[0])

    elif tipo == "3":
        senha = input("Senha do administrador: ")

        if senha != SENHA_ADMIN:
            print("\nSenha incorreta.")
            return

        print("\nLogin administrativo realizado com sucesso!")

        menu_admin()

    elif tipo == "0":
        return

    else:
        print("\nOpção inválida.")


def main():
    while True:
        print("\n===================================")
        print("             UBER 2")
        print("===================================")
        print("1 - Login")
        print("2 - Cadastrar usuário")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            login()

        elif opcao == "2":
            cadastrar_usuario()

        elif opcao == "0":
            print("\nObrigado por utilizar o Uber 2!")
            break

        else:
            print("\nOpção inválida.")


if __name__ == "__main__":
    main()
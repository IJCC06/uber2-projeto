from conexao import conectar

from usuarios import (
    cadastrar_usuario,
    solicitar_corrida,
    minhas_corridas,
    consultar_pagamentos,
    avaliar_corrida
)

from motoristas import (
    cadastrar_motorista,
    visualizar_corridas,
    aceitar_corrida,
    atualizar_status,
    cadastrar_veiculo,
    consultar_historico
)


# ==========================================
# CONFIGURAÇÕES
# ==========================================

SENHA_ADMIN = "Uber2Admin"


# ==========================================
# LOGIN DO USUÁRIO
# ==========================================

def login_usuario():

    email = input("E-mail: ")
    senha = input("Senha: ")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, email
        FROM usuarios
        WHERE email = ? AND senha = ?
    """, (email, senha))

    usuario = cursor.fetchone()

    conexao.close()

    if usuario:
        print(f"\nBem-vindo(a), {usuario[1]}!")
        print(f"Usuário conectado: ID {usuario[0]}")
        return usuario

    print("\nE-mail ou senha incorretos.")

    return None


# ==========================================
# LOGIN DO MOTORISTA
# ==========================================

def login_motorista():

    cpf = input("CPF: ")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, cpf, status
        FROM motoristas
        WHERE cpf = ?
    """, (cpf,))

    motorista = cursor.fetchone()

    conexao.close()

    if motorista is None:
        print("\nMotorista não encontrado.")
        return None

    if motorista[3] != "Ativo":
        print("\nEste motorista está inativo.")
        return None

    print(f"\nBem-vindo, {motorista[1]}!")
    print(f"Motorista conectado: ID {motorista[0]}")

    return motorista


# ==========================================
# LOGIN DO ADMINISTRADOR
# ==========================================

def login_administrador():

    senha = input("Senha do administrador: ")

    if senha == SENHA_ADMIN:

        print("\nAcesso administrativo autorizado!")

        return True

    print("\nSenha incorreta.")

    return False


# ==========================================
# MENU DO USUÁRIO
# ==========================================

def menu_usuario(id_usuario):

    while True:

        print("""
========================================
             MENU DO USUÁRIO
========================================

1 - Solicitar corrida
2 - Minhas corridas
3 - Consultar pagamentos
4 - Avaliar corrida

0 - Sair

========================================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            solicitar_corrida(id_usuario)

        elif opcao == "2":

            minhas_corridas(id_usuario)

        elif opcao == "3":

            consultar_pagamentos(id_usuario)

        elif opcao == "4":

            avaliar_corrida(id_usuario)

        elif opcao == "0":

            print("\nSaindo do menu do usuário...")
            break

        else:

            print("\nOpção inválida!")


# ==========================================
# MENU DO MOTORISTA
# ==========================================

def menu_motorista(id_motorista):

    while True:

        print("""
========================================
            MENU DO MOTORISTA
========================================

1 - Visualizar corridas disponíveis
2 - Aceitar corrida
3 - Atualizar status da corrida
4 - Cadastrar veículo
5 - Consultar histórico

0 - Sair

========================================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            visualizar_corridas(id_motorista)

        elif opcao == "2":

            aceitar_corrida(id_motorista)

        elif opcao == "3":

            atualizar_status(id_motorista)

        elif opcao == "4":

            cadastrar_veiculo(id_motorista)

        elif opcao == "5":

            consultar_historico(id_motorista)

        elif opcao == "0":

            print("\nSaindo do menu do motorista...")
            break

        else:

            print("\nOpção inválida!")


# ==========================================
# MENU DO ADMINISTRADOR
# ==========================================

def menu_administrador():

    while True:

        print("""
========================================
          MENU ADMINISTRADOR
========================================

1 - Gerenciar usuários
2 - Gerenciar motoristas
3 - Gerenciar veículos
4 - Gerenciar endereços
5 - Gerenciar corridas
6 - Gerenciar pagamentos
7 - Gerenciar avaliações
8 - Consultas e relatórios

0 - Sair

========================================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            print("\n===== GERENCIAR USUÁRIOS =====")

            print("""
1 - Listar usuários
2 - Editar usuário
3 - Excluir usuário
0 - Voltar
""")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":

                print("\nListagem de usuários")

            elif escolha == "2":

                print("\nEdição de usuário")

            elif escolha == "3":

                print("\nExclusão de usuário")

            elif escolha == "0":

                continue

            else:

                print("\nOpção inválida!")


        elif opcao == "2":

            print("\n===== GERENCIAR MOTORISTAS =====")

            print("""
1 - Listar motoristas
2 - Editar motorista
3 - Excluir motorista
0 - Voltar
""")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":

                print("\nListagem de motoristas")

            elif escolha == "2":

                print("\nEdição de motorista")

            elif escolha == "3":

                print("\nExclusão de motorista")

            elif escolha == "0":

                continue

            else:

                print("\nOpção inválida!")


        elif opcao == "3":

            print("\n===== GERENCIAR VEÍCULOS =====")

            print("""
1 - Listar veículos
2 - Editar veículo
3 - Excluir veículo
0 - Voltar
""")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":

                print("\nListagem de veículos")

            elif escolha == "2":

                print("\nEdição de veículo")

            elif escolha == "3":

                print("\nExclusão de veículo")

            elif escolha == "0":

                continue

            else:

                print("\nOpção inválida!")


        elif opcao == "4":

            print("\n===== GERENCIAR ENDEREÇOS =====")

            print("""
1 - Listar endereços
2 - Editar endereço
3 - Excluir endereço
0 - Voltar
""")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":

                print("\nListagem de endereços")

            elif escolha == "2":

                print("\nEdição de endereço")

            elif escolha == "3":

                print("\nExclusão de endereço")

            elif escolha == "0":

                continue

            else:

                print("\nOpção inválida!")


        elif opcao == "5":

            print("\n===== GERENCIAR CORRIDAS =====")

            print("""
1 - Listar corridas
2 - Editar corrida
3 - Excluir corrida
0 - Voltar
""")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":

                print("\nListagem de corridas")

            elif escolha == "2":

                print("\nEdição de corrida")

            elif escolha == "3":

                print("\nExclusão de corrida")

            elif escolha == "0":

                continue

            else:

                print("\nOpção inválida!")


        elif opcao == "6":

            print("\n===== GERENCIAR PAGAMENTOS =====")

            print("""
1 - Listar pagamentos
2 - Editar pagamento
3 - Excluir pagamento
0 - Voltar
""")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":

                print("\nListagem de pagamentos")

            elif escolha == "2":

                print("\nEdição de pagamento")

            elif escolha == "3":

                print("\nExclusão de pagamento")

            elif escolha == "0":

                continue

            else:

                print("\nOpção inválida!")


        elif opcao == "7":

            print("\n===== GERENCIAR AVALIAÇÕES =====")

            print("""
1 - Listar avaliações
2 - Editar avaliação
3 - Excluir avaliação
0 - Voltar
""")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":

                print("\nListagem de avaliações")

            elif escolha == "2":

                print("\nEdição de avaliação")

            elif escolha == "3":

                print("\nExclusão de avaliação")

            elif escolha == "0":

                continue

            else:

                print("\nOpção inválida!")


        elif opcao == "8":

            print("""
========================================
        CONSULTAS E RELATÓRIOS
========================================

1 - 5 corridas mais caras
2 - Motorista com mais corridas
3 - Forma de pagamento mais utilizada
4 - Usuários com mais corridas
5 - Motoristas disponíveis
6 - Histórico de uma corrida
7 - Total arrecadado em um período
8 - Média de avaliação dos motoristas
9 - Média geral dos motoristas
0 - Voltar
""")

            escolha = input("Escolha uma opção: ")

            if escolha == "0":

                continue

            else:

                print("\nConsulta selecionada.")


        elif opcao == "0":

            print("\nSaindo do menu administrativo...")
            break

        else:

            print("\nOpção inválida!")


# ==========================================
# ACESSO DO USUÁRIO
# ==========================================

def acesso_usuario():

    while True:

        print("""
========================================
           ACESSO DO USUÁRIO
========================================

1 - Fazer login
2 - Criar cadastro
0 - Voltar

========================================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            usuario = login_usuario()

            if usuario:

                id_usuario = usuario[0]

                menu_usuario(id_usuario)


        elif opcao == "2":

            cadastrar_usuario()


        elif opcao == "0":

            break


        else:

            print("\nOpção inválida!")


# ==========================================
# ACESSO DO MOTORISTA
# ==========================================

def acesso_motorista():

    while True:

        print("""
========================================
          ACESSO DO MOTORISTA
========================================

1 - Fazer login
2 - Criar cadastro
0 - Voltar

========================================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            motorista = login_motorista()

            if motorista:

                id_motorista = motorista[0]

                menu_motorista(id_motorista)


        elif opcao == "2":

            cadastrar_motorista()


        elif opcao == "0":

            break


        else:

            print("\nOpção inválida!")


# ==========================================
# ACESSO DO ADMINISTRADOR
# ==========================================

def acesso_administrador():

    if login_administrador():

        menu_administrador()


# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu_principal():

    while True:

        print("""
╔════════════════════════════════════════╗
║              🚗 UBER 2 🚗              ║
║        O inimigo agora é outro!       ║
╚════════════════════════════════════════╝

1 - 👤 Usuário comum
2 - 🚗 Motorista
3 - 👨‍💼 Administrador
0 - 🚪 Sair
""")

        opcao = input("Escolha uma opção: ")


        if opcao == "1":

            acesso_usuario()


        elif opcao == "2":

            acesso_motorista()


        elif opcao == "3":

            acesso_administrador()


        elif opcao == "0":

            print("""
========================================
       Obrigado por usar o Uber 2!
========================================
""")

            break


        else:

            print("\nOpção inválida!")


# ==========================================
# EXECUÇÃO DO PROGRAMA
# ==========================================

if __name__ == "__main__":

    menu_principal()
from conexao import criar_conexao
from python.usuario import Usuario
from python.seguranca import verificar_senha

def realizar_login_admin(email, senha):
    sql = '''
        SELECT id, nome, senha
        FROM administradores
        WHERE email = %s AND ativo = True
    '''

    con = criar_conexao()
    cursor = con.cursor()

    try:
        cursor.execute(sql, (email,))
        resposta = cursor.fetchone()

        if resposta is None:
            return None

        id_admin, nome, senha_hash = resposta

        if not verificar_senha(senha, senha_hash):
            return None

        return Usuario(
            id = id_admin,
            nome = nome,
            tipo = "admin"
        )

    finally:
        cursor.close()
        con.close()


def realizar_login_usuario(email, senha):
    sql = '''
        SELECT id, nome, senha
        FROM usuarios
        WHERE email = %s
    '''

    con = criar_conexao()
    cursor = con.cursor()

    try:
        cursor.execute(sql, (email,))
        resposta = cursor.fetchone()

        if resposta is None:
            return None

        id_usuario, nome, senha_hash = resposta

        if not verificar_senha(senha, senha_hash):
            return None

        return Usuario(
            id = id_usuario,
            nome = nome,
            tipo = "usuario"
        )

    finally:
        cursor.close()
        con.close()


def realizar_login_motorista(cpf):
    sql = '''
        SELECT id, nome
        FROM motoristas
        WHERE cpf = %s
    '''
    
    con = criar_conexao()
    cursor = con.cursor()

    try:
        cursor.execute(sql, (cpf,))
        resposta = cursor.fetchone()

        if resposta:
            return Usuario(
                id = resposta[0],
                nome = resposta[1],
                tipo = "motorista"
            )

        return None

    finally:
        cursor.close()
        con.close()
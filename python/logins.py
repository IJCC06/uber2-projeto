from conexao import criar_conexao

def realizar_login_admin(email, senha):
    sql = '''
        SELECT email, senha, ativo
        FROM administradores
        WHERE email = %s AND senha = %s AND ativo = True
    '''

    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(sql, (email, senha))
    resposta = cursor.fetchone()
    con.close()

    if resposta:
        return True
    else:
        return False


def realizar_login_usuario(email, senha):
    sql = '''
        SELECT email, senha
        FROM usuarios
        WHERE email = %s AND senha = %s
    '''

    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(sql, (email, senha))
    resposta = cursor.fetchone()
    con.close()

    if resposta:
        return True
    else:
        return False


def realizar_login_motorista(cpf):
    sql = '''
        SELECT cpf
        FROM motoristas
        WHERE cpf = %s
    '''
    
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(sql, (cpf,))
    resposta = cursor.fetchone()
    con.close()
    
    if resposta:
        return True
    else:
        return False
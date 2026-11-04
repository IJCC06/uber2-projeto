from flask import Flask, jsonify, render_template, url_for, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import psycopg2
from conexao import criar_conexao
import os

from python.seguranca import criar_hash_senha
from python.usuario import Usuario
from python.logins import realizar_login_admin, realizar_login_usuario, realizar_login_motorista


uber2 = Flask(__name__)

uber2.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(uber2)
login_manager.login_view = "login"

#Retorna as Informações do Usuário Logado
@login_manager.user_loader
def carregar_usuario(user_id):
    try:
        tipo, id_usuario = user_id.split(":", 1)
        id_usuario = int(id_usuario)
    except (ValueError, AttributeError):
        return None

    con = criar_conexao()
    cursor = con.cursor()

    try:
        if tipo == "usuario":
            cursor.execute(
                "SELECT id, nome FROM usuarios WHERE id = %s",
                (id_usuario,)
            )

        elif tipo == "motorista":
            cursor.execute(
                "SELECT id, nome FROM motoristas WHERE id = %s",
                (id_usuario,)
            )

        elif tipo == "admin":
            cursor.execute(
                "SELECT id, nome FROM administradores WHERE id = %s",
                (id_usuario,)
            )

        else:
            return None

        resultado = cursor.fetchone()

        if resultado is None:
            return None


        return Usuario(
            id = resultado[0],
            nome = resultado[1],
            tipo = tipo
        )

    finally:
        cursor.close()
        con.close()



# Renderiza a Tela de Login
@uber2.route('/', methods=['GET'])
def login():
    return render_template('logins/login.html')


# Renderiza a Tela de Cadastro
@uber2.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('logins/cadastro.html')

    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip().lower()
    telefone = request.form.get('telefone', '').strip()
    senha = request.form.get('senha', '')
    confirmar_senha = request.form.get('confirmar_senha', '')

    if not all([nome, email, telefone, senha, confirmar_senha]):
        return render_template(
            'logins/cadastro.html',
            erro='Preencha todos os campos.'
        )

    if len(nome) > 100 or len(email) > 150 or len(telefone) > 20:
        return render_template(
            'logins/cadastro.html',
            erro='Um ou mais campos ultrapassaram o limite permitido.'
        )

    if len(senha) < 8:
        return render_template(
            'logins/cadastro.html',
            erro='A senha deve possuir pelo menos 8 caracteres.'
        )

    if senha != confirmar_senha:
        return render_template(
            'logins/cadastro.html',
            erro='As senhas não coincidem.'
        )

    senha_hash = criar_hash_senha(senha)

    con = criar_conexao()
    cursor = con.cursor()

    try:
        cursor.execute(
            "SELECT id FROM usuarios WHERE email = %s",
            (email,)
        )

        if cursor.fetchone():
            return render_template(
                'logins/cadastro.html',
                erro='Esse e-mail já está cadastrado.'
            )

        cursor.execute(
            '''
            INSERT INTO usuarios (nome, email, telefone, senha)
            VALUES (%s, %s, %s, %s)
            ''',
            (nome, email, telefone, senha_hash)
        )

        con.commit()

        return render_template(
            'logins/cadastro.html',
            sucesso = 'Cadastro realizado com sucesso! Você já pode fazer login.'
        )

    except psycopg2.errors.UniqueViolation:
        con.rollback()

        return render_template(
            'logins/cadastro.html',
            erro = 'Este e-mail já está cadastrado.'
        )

    except psycopg2.Error:
        con.rollback()

        return render_template(
            'logins/cadastro.html',
            erro = 'Não foi possível realizar o cadastro. Tente novamente.'
        )

    finally:
        cursor.close()
        con.close()


# Validação do Login do Usuário
@uber2.route('/login/usuario', methods=['POST'])
def login_usuario():
    email = request.form["email"]
    senha = request.form["password"]

    usuario = realizar_login_usuario(email, senha)

    if usuario:
        login_user(usuario)
        return redirect(url_for('home_usuarios'))

    return redirect(url_for('login'))


# Validação do Login do Motorista
@uber2.route('/login/motorista', methods=['POST'])
def login_motorista():
    cpf = request.form["cpf"]

    motorista = realizar_login_motorista(cpf)

    if motorista:
        login_user(motorista)
        return redirect(url_for('home_motorista'))
    
    return redirect(url_for('login'))


# Validação do Login Administrativo
@uber2.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        admin = realizar_login_admin(email, senha)

        if admin:
            login_user(admin)
            return redirect(url_for('home_admin'))
        
        return render_template('logins/login_admin.html')

    return render_template('logins/login_admin.html')


# Renderiza a Tela Inicial dos Usuários
@uber2.route('/usuario/home', methods=['GET'])
@login_required
def home_usuarios():
    if current_user.tipo != "usuario":
        abort(403)
    
    return render_template('/usuarios/home_usuarios.html')

# Renderizar a Tela Inicial dos Motoristas
@uber2.route('/motorista/home', methods=['GET'])
@login_required
def home_motorista():
    if current_user.tipo != "motorista":
        abort(403)

    return render_template('motoristas/home_motorista.html')

# Renderizar a Tela Inicial dos Admins
@uber2.route('/admin/home', methods=['GET'])
@login_required
def home_admin():
    if current_user.tipo != "admin":
        abort(403)

    return render_template('admins/home_admin.html')


@uber2.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    uber2.run(debug=True)
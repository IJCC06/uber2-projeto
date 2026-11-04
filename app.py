from flask import Flask, jsonify, render_template, url_for, redirect, request
from flask_login import LoginManager
import psycopg2
from conexao import criar_conexao
import os

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

# Validação do Login do Usuário
@uber2.route('/login/usuario', methods=['POST'])
def login_usuario():
    email = request.form["email"]
    senha = request.form["password"]

    logado = realizar_login_usuario(email, senha)
    if logado:
        return redirect(url_for('home_usuarios'))
    else:
        return redirect(url_for('login'))

# Validação do Login do Motorista
@uber2.route('/login/motorista', methods=['POST'])
def login_motorista():
    cpf = request.form["cpf"]

    logado = realizar_login_motorista(cpf)
    if logado:
        return render_template('motorista/home_motorista.html')
    else:
        return redirect(url_for('login'))

# Validação do Login Administrativo
@uber2.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        logado = realizar_login_admin(email, senha)
        if logado:
            return render_template('admins/home_admin.html')
        else:
            return render_template('logins/login_admin.html')

    return render_template('logins/login_admin.html')


# Renderiza a Tela Inicial dos Usuários
@uber2.route('/usuarios/home', methods=['GET'])
def home_usuarios():
    return render_template('/usuarios/home_usuarios.html')


if __name__ == "__main__":
    uber2.run(debug=True)
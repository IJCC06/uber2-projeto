from flask import Flask, jsonify, render_template, url_for, redirect, request
import psycopg2
from conexao import criar_conexao

from python.logins import realizar_login_admin, realizar_login_usuario, realizar_login_motorista


uber2 = Flask(__name__)


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
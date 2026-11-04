from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request
)
from flask_login import login_user, logout_user, login_required
import psycopg2

from conexao import criar_conexao
from python.seguranca import criar_hash_senha
from python.logins import (
    realizar_login_admin,
    realizar_login_usuario,
    realizar_login_motorista
)

auth = Blueprint("auth", __name__)


#Tela de Login
@auth.route("/", methods=["GET"])
def login():
    return render_template("logins/login.html")


# Cadastro de Usuários
@auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("logins/cadastro.html")

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    telefone = request.form.get("telefone", "").strip()
    senha = request.form.get("senha", "")
    confirmar_senha = request.form.get("confirmar_senha", "")

    if not all([nome, email, telefone, senha, confirmar_senha]):
        return render_template(
            "logins/cadastro.html",
            erro="Preencha todos os campos."
        )

    if len(nome) > 100 or len(email) > 150 or len(telefone) > 20:
        return render_template(
            "logins/cadastro.html",
            erro="Um ou mais campos ultrapassaram o limite permitido."
        )

    if len(senha) < 8:
        return render_template(
            "logins/cadastro.html",
            erro="A senha deve possuir pelo menos 8 caracteres."
        )

    if senha != confirmar_senha:
        return render_template(
            "logins/cadastro.html",
            erro="As senhas não coincidem."
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
                "logins/cadastro.html",
                erro="Esse e-mail já está cadastrado."
            )

        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, telefone, senha)
            VALUES (%s, %s, %s, %s)
            """,
            (nome, email, telefone, senha_hash)
        )

        con.commit()

        return render_template(
            "logins/cadastro.html",
            sucesso="Cadastro realizado com sucesso! Você já pode fazer login."
        )

    except psycopg2.errors.UniqueViolation:
        con.rollback()

        return render_template(
            "logins/cadastro.html",
            erro="Este e-mail já está cadastrado."
        )

    except psycopg2.Error:
        con.rollback()

        return render_template(
            "logins/cadastro.html",
            erro="Não foi possível realizar o cadastro. Tente novamente."
        )

    finally:
        cursor.close()
        con.close()


# Login de Usuário
@auth.route("/login/usuario", methods=["POST"])
def login_usuario():
    email = request.form["email"]
    senha = request.form["password"]

    usuario = realizar_login_usuario(email, senha)

    if usuario:
        login_user(usuario)
        return redirect(url_for("usuarios.home"))

    return render_template(
        "logins/login.html",
        erro="E-mail ou senha incorretos."
    )


# Login de Motorista
@auth.route("/login/motorista", methods=["POST"])
def login_motorista():
    cpf = request.form["cpf"]
    senha = request.form["password"]

    motorista = realizar_login_motorista(cpf, senha)

    if motorista:
        login_user(motorista)
        return redirect(url_for("motoristas.home"))

    return render_template(
        "logins/login.html",
        erro="CPF ou senha inválidos."
    )


# Login de Administrador
@auth.route("/login/admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        admin = realizar_login_admin(email, senha)

        if admin:
            login_user(admin)
            return redirect(url_for("admins.home"))

        return render_template(
            "logins/login_admin.html",
            erro="E-mail ou senha incorretos."
        )

    return render_template("logins/login_admin.html")


# Logout
@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
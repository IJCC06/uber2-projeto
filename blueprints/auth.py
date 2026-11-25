import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import (
    Blueprint,
    current_app,
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

_RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
_RECAPTCHA_ERROR = (
    "Não foi possível validar o CAPTCHA. Tente novamente."
)


def _captcha_configurado():
    return bool(
        current_app.config.get("RECAPTCHA_SITE_KEY")
        and current_app.config.get("RECAPTCHA_SECRET_KEY")
    )


def _renderizar_login(template, **contexto):
    configurado = _captcha_configurado()
    return render_template(
        template,
        recaptcha_configurado=configurado,
        recaptcha_site_key=(
            current_app.config.get("RECAPTCHA_SITE_KEY") if configurado else None
        ),
        **contexto,
    )


def _verificar_recaptcha():
    token = request.form.get("g-recaptcha-response", "").strip()
    if not token:
        return False

    secret_key = current_app.config.get("RECAPTCHA_SECRET_KEY")
    if not secret_key or not current_app.config.get("RECAPTCHA_SITE_KEY"):
        current_app.logger.error(
            "As chaves do Google reCAPTCHA não estão configuradas."
        )
        return False

    payload = urlencode(
        {"secret": secret_key, "response": token}
    ).encode("ascii")
    requisicao = Request(
        _RECAPTCHA_VERIFY_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urlopen(requisicao, timeout=5) as resposta:
            resultado = json.loads(resposta.read(65536).decode("utf-8"))
    except (
        URLError,
        TimeoutError,
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ):
        current_app.logger.exception("Falha ao consultar o Google reCAPTCHA.")
        return False

    if not isinstance(resultado, dict):
        current_app.logger.error("Resposta inválida do Google reCAPTCHA.")
        return False

    if resultado.get("success") is not True:
        current_app.logger.warning(
            "Google reCAPTCHA rejeitou a tentativa de login: %s",
            resultado.get("error-codes", []),
        )
        return False

    return True


#Tela de Login
@auth.route("/", methods=["GET"])
def login():
    return _renderizar_login("logins/login.html")


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


@auth.route("/cadastro/motorista", methods=["GET", "POST"])
def cadastro_motorista():
    if request.method == "GET":
        return render_template("logins/cadastro_motorista.html")

    nome = request.form.get("nome", "").strip()
    cpf = request.form.get("cpf", "").strip()
    telefone = request.form.get("telefone", "").strip()
    cnh = request.form.get("cnh", "").strip()
    senha = request.form.get("senha", "")
    confirmar_senha = request.form.get("confirmar_senha", "")

    if not all([nome, cpf, telefone, cnh, senha, confirmar_senha]):
        return render_template(
            "logins/cadastro_motorista.html",
            erro="Preencha todos os campos.",
        )

    if len(nome) > 100 or len(cpf) > 14 or len(telefone) > 20 or len(cnh) > 20:
        return render_template(
            "logins/cadastro_motorista.html",
            erro="Um ou mais campos ultrapassaram o limite permitido.",
        )

    if len(senha) < 8:
        return render_template(
            "logins/cadastro_motorista.html",
            erro="A senha deve possuir pelo menos 8 caracteres.",
        )

    if senha != confirmar_senha:
        return render_template(
            "logins/cadastro_motorista.html",
            erro="As senhas não coincidem.",
        )

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO motoristas
                    (nome, cpf, telefone, cnh, senha, status, disponivel)
                VALUES (%s, %s, %s, %s, %s, 'Inativo', FALSE)
                """,
                (nome, cpf, telefone, cnh, criar_hash_senha(senha)),
            )
        conexao.commit()
    except psycopg2.errors.UniqueViolation:
        if conexao is not None:
            conexao.rollback()
        return render_template(
            "logins/cadastro_motorista.html",
            erro="Este CPF ou CNH já está cadastrado.",
        )
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao cadastrar um motorista.")
        return render_template(
            "logins/cadastro_motorista.html",
            erro="Não foi possível realizar o cadastro. Tente novamente.",
        )
    finally:
        if conexao is not None:
            conexao.close()

    return render_template(
        "logins/cadastro_motorista.html",
        sucesso=(
            "Cadastro recebido. Sua conta ficará inativa até a aprovação "
            "de um administrador."
        ),
    )


# Login de Usuário
@auth.route("/login/usuario", methods=["POST"])
def login_usuario():
    if not _verificar_recaptcha():
        return _renderizar_login("logins/login.html", erro=_RECAPTCHA_ERROR)

    email = request.form["email"]
    senha = request.form["password"]

    usuario = realizar_login_usuario(email, senha)

    if usuario:
        login_user(usuario)
        return redirect(url_for("usuarios.home"))

    return _renderizar_login(
        "logins/login.html",
        erro="E-mail ou senha incorretos."
    )


# Login de Motorista
@auth.route("/login/motorista", methods=["POST"])
def login_motorista():
    if not _verificar_recaptcha():
        return _renderizar_login("logins/login.html", erro=_RECAPTCHA_ERROR)

    cpf = request.form["cpf"]
    senha = request.form["password"]

    motorista = realizar_login_motorista(cpf, senha)

    if motorista:
        login_user(motorista)
        return redirect(url_for("motoristas.home"))

    return _renderizar_login(
        "logins/login.html",
        erro="CPF ou senha inválidos."
    )


# Login de Administrador
@auth.route("/login/admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        if not _verificar_recaptcha():
            return _renderizar_login(
                "logins/login_admin.html",
                erro=_RECAPTCHA_ERROR,
            )

        email = request.form["email"]
        senha = request.form["password"]

        admin = realizar_login_admin(email, senha)

        if admin:
            login_user(admin)
            return redirect(url_for("admins.home"))

        return _renderizar_login(
            "logins/login_admin.html",
            erro="E-mail ou senha incorretos."
        )

    return _renderizar_login("logins/login_admin.html")


# Logout
@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
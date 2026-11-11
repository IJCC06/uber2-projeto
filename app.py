from flask import Flask, render_template
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

from conexao import criar_conexao
from python.usuario import Usuario

load_dotenv()


uber2 = Flask(__name__, static_folder="public/static")
app = uber2

uber2.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if not uber2.config["SECRET_KEY"]:
    raise RuntimeError("A variável SECRET_KEY não foi configurada.")


login_manager = LoginManager()
login_manager.init_app(uber2)
login_manager.login_view = "auth.login"


# Retorna as informações do usuário logado
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
                "SELECT id, nome FROM usuarios WHERE id = %s AND ativo = TRUE",
                (id_usuario,)
            )

        elif tipo == "motorista":
            cursor.execute(
                "SELECT id, nome FROM motoristas WHERE id = %s AND status = 'Ativo'",
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
            id=resultado[0],
            nome=resultado[1],
            tipo=tipo
        )

    finally:
        cursor.close()
        con.close()


# Importação dos Blueprints
from blueprints.auth import auth
from blueprints.usuarios import usuarios
from blueprints.motoristas import motoristas
from blueprints.admins import admins


# Registro dos Blueprints
uber2.register_blueprint(auth)
uber2.register_blueprint(usuarios)
uber2.register_blueprint(motoristas)
uber2.register_blueprint(admins)

_MENSAGENS_ERRO_HTTP = {
    400: (
        "Requisição inválida",
        "Confira as informações enviadas e tente novamente.",
    ),
    403: (
        "Acesso não autorizado",
        "Você não tem permissão para acessar esta página.",
    ),
    404: (
        "Página não encontrada",
        "O endereço pode estar incorreto ou a página pode ter sido removida.",
    ),
    405: (
        "Método não permitido",
        "Esta ação não está disponível por esse tipo de solicitação.",
    ),
    500: (
        "Erro interno",
        "Ocorreu um problema inesperado. Tente novamente mais tarde.",
    ),
}


@uber2.errorhandler(HTTPException)
def tratar_erro_http(erro):
    status_code = erro.code or 500
    titulo, mensagem = _MENSAGENS_ERRO_HTTP.get(
        status_code,
        ("Não foi possível processar a solicitação", "Tente novamente."),
    )
    resposta = erro.get_response()
    resposta.set_data(
        render_template(
            "errors/error.html",
            status_code=status_code,
            titulo=titulo,
            mensagem=mensagem,
        )
    )
    resposta.content_type = "text/html; charset=utf-8"
    return resposta


if __name__ == "__main__":
    uber2.run(debug=True)

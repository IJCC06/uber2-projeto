from flask import Flask
from flask_login import LoginManager
import os

from conexao import criar_conexao
from python.usuario import Usuario

# E-mail Admin Teste = admin.bdfb6e6958@example.test


uber2 = Flask(__name__)

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


if __name__ == "__main__":
    uber2.run(debug=True)
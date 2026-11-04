
import psycopg2
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, current_user

from conexao import criar_conexao

usuarios = Blueprint("usuarios", __name__, url_prefix="/usuario")


@usuarios.route("/home", methods=["GET"])
@login_required
def home():
    if current_user.tipo != "usuario":
        abort(403)

    return render_template("usuarios/home_usuarios.html")


@usuarios.route("/corridas/solicitar", methods=["GET", "POST"])
@login_required
def solicitar_corrida():
    if current_user.tipo != "usuario":
        abort(403)

    if request.method == "GET":
        return render_template("usuarios/solicitar_corrida.html")

    origem = request.form.get("origem", "").strip()
    destino = request.form.get("destino", "").strip()

    if not origem or not destino:
        return render_template(
            "usuarios/solicitar_corrida.html",
            erro="Preencha os endereços de origem e destino.",
        ), 400

    if len(origem) > 100 or len(destino) > 100:
        return render_template(
            "usuarios/solicitar_corrida.html",
            erro="Cada endereço deve ter no máximo 100 caracteres.",
        ), 400

    if origem.casefold() == destino.casefold():
        return render_template(
            "usuarios/solicitar_corrida.html",
            erro="A origem e o destino não podem ser iguais.",
        ), 400

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO corridas (id_usuario, origem, destino)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (current_user.id, origem, destino),
            )
            corrida_id = cursor.fetchone()[0]

        conexao.commit()
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao registrar uma solicitação de corrida.")
        return render_template(
            "usuarios/solicitar_corrida.html",
            erro="Não foi possível solicitar a corrida. Tente novamente.",
        ), 500
    finally:
        if conexao is not None:
            conexao.close()

    flash(f"Corrida #{corrida_id} solicitada com sucesso.", "success")
    return redirect(url_for("usuarios.solicitar_corrida"))

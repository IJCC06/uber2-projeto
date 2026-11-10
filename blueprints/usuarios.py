
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


@usuarios.route("/corridas", methods=["GET"])
@login_required
def minhas_corridas():
    if current_user.tipo != "usuario":
        abort(403)

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    c.id,
                    c.origem,
                    c.destino,
                    c.data_hora,
                    c.status,
                    c.distancia_km,
                    c.valor,
                    m.nome
                FROM corridas AS c
                LEFT JOIN motoristas AS m ON m.id = c.id_motorista
                WHERE c.id_usuario = %s
                ORDER BY c.data_hora DESC, c.id DESC
                """,
                (current_user.id,),
            )
            corridas = [
                {
                    "id": linha[0],
                    "origem": linha[1],
                    "destino": linha[2],
                    "data_hora": linha[3],
                    "status": linha[4],
                    "distancia_km": linha[5],
                    "valor": linha[6],
                    "motorista": linha[7],
                }
                for linha in cursor.fetchall()
            ]
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(
            "Falha ao carregar o histórico de corridas do usuário."
        )
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return render_template("usuarios/minhas_corridas.html", corridas=corridas)


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


@usuarios.route("/pagamentos", methods=["GET", "POST"])
@login_required
def pagamentos():
    if current_user.tipo != "usuario":
        abort(403)

    conexao = None
    try:
        conexao = criar_conexao()

        if request.method == "POST":
            forma_pagamento = request.form.get("forma_pagamento", "")
            corrida_id_texto = request.form.get("corrida_id", "")
            formas_validas = {"Pix", "Dinheiro", "Cartão"}

            if forma_pagamento not in formas_validas:
                flash("Selecione uma forma de pagamento válida.", "error")
            else:
                try:
                    corrida_id = int(corrida_id_texto)
                    if corrida_id <= 0:
                        raise ValueError
                except ValueError:
                    flash("Corrida inválida.", "error")
                else:
                    with conexao.cursor() as cursor:
                        cursor.execute(
                            """
                            INSERT INTO pagamentos
                                (id_corrida, forma_pagamento, valor, status)
                            SELECT c.id, %s, c.valor, 'Pendente'
                            FROM corridas AS c
                            WHERE c.id = %s
                              AND c.id_usuario = %s
                              AND c.status = 'Finalizada'
                              AND c.valor IS NOT NULL
                            ON CONFLICT (id_corrida) DO NOTHING
                            RETURNING id
                            """,
                            (forma_pagamento, corrida_id, current_user.id),
                        )
                        pagamento = cursor.fetchone()

                    if pagamento is None:
                        conexao.rollback()
                        flash(
                            "Não foi possível registrar. A corrida precisa ser sua, "
                            "estar finalizada e ainda não ter pagamento.",
                            "error",
                        )
                    else:
                        conexao.commit()
                        flash(
                            "Forma de pagamento registrada como pendente. "
                            "A cobrança ainda não foi processada.",
                            "success",
                        )

            return redirect(url_for("usuarios.pagamentos"))

        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    c.id,
                    c.origem,
                    c.destino,
                    c.distancia_km,
                    c.valor,
                    p.forma_pagamento,
                    p.status,
                    p.data_pagamento
                FROM corridas AS c
                LEFT JOIN pagamentos AS p ON p.id_corrida = c.id
                WHERE c.id_usuario = %s
                  AND c.status = 'Finalizada'
                ORDER BY c.data_hora DESC
                """,
                (current_user.id,),
            )
            corridas = [
                {
                    "id": linha[0],
                    "origem": linha[1],
                    "destino": linha[2],
                    "distancia_km": linha[3],
                    "valor": linha[4],
                    "forma_pagamento": linha[5],
                    "status_pagamento": linha[6],
                    "data_pagamento": linha[7],
                }
                for linha in cursor.fetchall()
            ]
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao carregar ou registrar pagamentos do usuário.")
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return render_template("usuarios/pagamentos.html", corridas=corridas)

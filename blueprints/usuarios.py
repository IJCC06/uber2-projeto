
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
from python.seguranca import criar_hash_senha, verificar_senha

usuarios = Blueprint("usuarios", __name__, url_prefix="/usuario")


@usuarios.route("/home", methods=["GET"])
@login_required
def home():
    if current_user.tipo != "usuario":
        abort(403)

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(*) FILTER (WHERE c.status = 'Finalizada'),
                    COUNT(*) FILTER (
                        WHERE c.status IN ('Aceita', 'Em andamento')
                    ),
                    COUNT(p.id) FILTER (WHERE p.status = 'Pendente')
                FROM corridas AS c
                LEFT JOIN pagamentos AS p ON p.id_corrida = c.id
                WHERE c.id_usuario = %s
                """,
                (current_user.id,),
            )
            resumo = cursor.fetchone()

            cursor.execute(
                """
                SELECT
                    c.id,
                    c.origem,
                    c.destino,
                    c.data_hora,
                    c.status,
                    c.valor,
                    m.nome
                FROM corridas AS c
                LEFT JOIN motoristas AS m ON m.id = c.id_motorista
                WHERE c.id_usuario = %s
                ORDER BY c.data_hora DESC, c.id DESC
                LIMIT 5
                """,
                (current_user.id,),
            )
            corridas_recentes = [
                {
                    "id": linha[0],
                    "origem": linha[1],
                    "destino": linha[2],
                    "data_hora": linha[3],
                    "status": linha[4],
                    "valor": linha[5],
                    "motorista": linha[6],
                }
                for linha in cursor.fetchall()
            ]
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao carregar o painel do usuário.")
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return render_template(
        "usuarios/home_usuarios.html",
        corridas_realizadas=resumo[0],
        corridas_ativas=resumo[1],
        pagamentos_pendentes=resumo[2],
        corridas_recentes=corridas_recentes,
    )


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
                    m.nome,
                    a.nota,
                    a.comentario
                FROM corridas AS c
                LEFT JOIN motoristas AS m ON m.id = c.id_motorista
                LEFT JOIN avaliacoes AS a ON a.id_corrida = c.id
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
                    "nota": linha[8],
                    "comentario": linha[9],
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


@usuarios.route("/corridas/<int:corrida_id>/cancelar", methods=["POST"])
@login_required
def cancelar_corrida(corrida_id):
    if current_user.tipo != "usuario":
        abort(403)

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                UPDATE corridas
                SET status = 'Cancelada'
                WHERE id = %s
                  AND id_usuario = %s
                  AND status = 'Solicitada'
                RETURNING id
                """,
                (corrida_id, current_user.id),
            )
            corrida = cursor.fetchone()

            if corrida is None:
                conexao.rollback()
                flash(
                    "Esta corrida não está mais disponível para cancelamento.",
                    "error",
                )
                return redirect(url_for("usuarios.minhas_corridas"))

            cursor.execute(
                """
                INSERT INTO historico_corridas
                    (id_corrida, status_anterior, novo_status)
                VALUES (%s, 'Solicitada', 'Cancelada')
                """,
                (corrida_id,),
            )

        conexao.commit()
        flash(f"Corrida #{corrida_id} cancelada.", "success")
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao cancelar a corrida %s.", corrida_id)
        flash("Não foi possível cancelar a corrida. Tente novamente.", "error")
    finally:
        if conexao is not None:
            conexao.close()

    return redirect(url_for("usuarios.minhas_corridas"))


@usuarios.route("/corridas/<int:corrida_id>/avaliar", methods=["POST"])
@login_required
def avaliar_corrida(corrida_id):
    if current_user.tipo != "usuario":
        abort(403)

    try:
        nota = int(request.form.get("nota", ""))
    except ValueError:
        flash("Selecione uma nota de 1 a 5.", "error")
        return redirect(url_for("usuarios.minhas_corridas"))

    if nota < 1 or nota > 5:
        flash("A nota deve estar entre 1 e 5.", "error")
        return redirect(url_for("usuarios.minhas_corridas"))

    comentario = request.form.get("comentario", "").strip()
    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO avaliacoes (id_corrida, nota, comentario)
                SELECT c.id, %s, NULLIF(%s, '')
                FROM corridas AS c
                WHERE c.id = %s
                  AND c.id_usuario = %s
                  AND c.status = 'Finalizada'
                  AND c.id_motorista IS NOT NULL
                ON CONFLICT (id_corrida) DO NOTHING
                RETURNING id
                """,
                (nota, comentario, corrida_id, current_user.id),
            )
            avaliacao = cursor.fetchone()

        if avaliacao is None:
            conexao.rollback()
            flash(
                "Não foi possível avaliar. A corrida precisa ser sua, "
                "estar finalizada e ainda não ter avaliação.",
                "error",
            )
        else:
            conexao.commit()
            flash("Avaliação registrada com sucesso.", "success")
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(
            "Falha ao registrar avaliação da corrida %s.", corrida_id
        )
        flash("Não foi possível registrar a avaliação. Tente novamente.", "error")
    finally:
        if conexao is not None:
            conexao.close()

    return redirect(url_for("usuarios.minhas_corridas"))


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


@usuarios.route("/conta", methods=["GET", "POST"])
@login_required
def conta():
    if current_user.tipo != "usuario":
        abort(403)

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefone = request.form.get("telefone", "").strip()
        senha_atual = request.form.get("senha_atual", "")
        nova_senha = request.form.get("nova_senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")
        alterar_senha = bool(nova_senha or confirmar_senha)

        if not nome or not email or not telefone:
            flash("Nome, e-mail e telefone são obrigatórios.", "error")
            return redirect(url_for("usuarios.conta"))

        if len(nome) > 100 or len(email) > 150 or len(telefone) > 20:
            flash("Um ou mais campos ultrapassaram o limite permitido.", "error")
            return redirect(url_for("usuarios.conta"))

        if alterar_senha:
            if not senha_atual:
                flash("Informe sua senha atual para definir uma nova senha.", "error")
                return redirect(url_for("usuarios.conta"))
            if len(nova_senha) < 8:
                flash("A nova senha deve possuir pelo menos 8 caracteres.", "error")
                return redirect(url_for("usuarios.conta"))
            if nova_senha != confirmar_senha:
                flash("A nova senha e a confirmação não coincidem.", "error")
                return redirect(url_for("usuarios.conta"))

        conexao = None
        try:
            conexao = criar_conexao()
            with conexao.cursor() as cursor:
                if alterar_senha:
                    cursor.execute(
                        "SELECT senha FROM usuarios WHERE id = %s FOR UPDATE",
                        (current_user.id,),
                    )
                    credenciais = cursor.fetchone()
                    if credenciais is None:
                        conexao.rollback()
                        abort(404)
                    if not verificar_senha(senha_atual, credenciais[0]):
                        conexao.rollback()
                        flash("A senha atual está incorreta.", "error")
                        return redirect(url_for("usuarios.conta"))

                    cursor.execute(
                        """
                        UPDATE usuarios
                        SET nome = %s, email = %s, telefone = %s, senha = %s
                        WHERE id = %s
                        RETURNING id
                        """,
                        (
                            nome,
                            email,
                            telefone,
                            criar_hash_senha(nova_senha),
                            current_user.id,
                        ),
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE usuarios
                        SET nome = %s, email = %s, telefone = %s
                        WHERE id = %s
                        RETURNING id
                        """,
                        (nome, email, telefone, current_user.id),
                    )

                usuario = cursor.fetchone()

            if usuario is None:
                conexao.rollback()
                abort(404)

            conexao.commit()
        except psycopg2.errors.UniqueViolation:
            if conexao is not None:
                conexao.rollback()
            flash("Esse e-mail já está cadastrado em outra conta.", "error")
            return redirect(url_for("usuarios.conta"))
        except psycopg2.Error:
            if conexao is not None:
                conexao.rollback()
            current_app.logger.exception(
                "Falha ao atualizar a conta do usuário %s.",
                current_user.id,
            )
            abort(500)
        finally:
            if conexao is not None:
                conexao.close()

        flash("Seus dados foram atualizados com sucesso.", "success")
        return redirect(url_for("usuarios.conta"))

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT nome, email, telefone
                FROM usuarios
                WHERE id = %s
                """,
                (current_user.id,),
            )
            usuario = cursor.fetchone()
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(
            "Falha ao carregar a conta do usuário %s.",
            current_user.id,
        )
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    if usuario is None:
        abort(404)

    return render_template(
        "usuarios/conta.html",
        usuario={"nome": usuario[0], "email": usuario[1], "telefone": usuario[2]},
    )

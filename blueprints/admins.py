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

admins = Blueprint(
    "admins",
    __name__,
    url_prefix="/admin"
)


@admins.route("/conta", methods=["GET", "POST"])
@login_required
def conta():
    if current_user.tipo != "admin":
        abort(403)

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha_atual = request.form.get("senha_atual", "")
        nova_senha = request.form.get("nova_senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")
        alterar_senha = bool(nova_senha or confirmar_senha)

        if not nome or not email:
            flash("Nome e e-mail são obrigatórios.", "error")
            return redirect(url_for("admins.conta"))

        if len(nome) > 100 or len(email) > 255:
            flash("Um ou mais campos ultrapassaram o limite permitido.", "error")
            return redirect(url_for("admins.conta"))

        if alterar_senha:
            if not senha_atual:
                flash("Informe sua senha atual para definir uma nova senha.", "error")
                return redirect(url_for("admins.conta"))
            if len(nova_senha) < 8:
                flash("A nova senha deve possuir pelo menos 8 caracteres.", "error")
                return redirect(url_for("admins.conta"))
            if nova_senha != confirmar_senha:
                flash("A nova senha e a confirmação não coincidem.", "error")
                return redirect(url_for("admins.conta"))

        conexao = None
        try:
            conexao = criar_conexao()
            with conexao.cursor() as cursor:
                if alterar_senha:
                    cursor.execute(
                        "SELECT senha FROM administradores WHERE id = %s FOR UPDATE",
                        (current_user.id,),
                    )
                    credenciais = cursor.fetchone()
                    if credenciais is None:
                        conexao.rollback()
                        abort(404)
                    if not verificar_senha(senha_atual, credenciais[0]):
                        conexao.rollback()
                        flash("A senha atual está incorreta.", "error")
                        return redirect(url_for("admins.conta"))

                    cursor.execute(
                        """
                        UPDATE administradores
                        SET nome = %s, email = %s, senha = %s
                        WHERE id = %s
                        RETURNING id
                        """,
                        (nome, email, criar_hash_senha(nova_senha), current_user.id),
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE administradores
                        SET nome = %s, email = %s
                        WHERE id = %s
                        RETURNING id
                        """,
                        (nome, email, current_user.id),
                    )

                administrador = cursor.fetchone()

            if administrador is None:
                conexao.rollback()
                abort(404)

            conexao.commit()
        except psycopg2.errors.UniqueViolation:
            if conexao is not None:
                conexao.rollback()
            flash("Esse e-mail já está cadastrado em outra conta.", "error")
            return redirect(url_for("admins.conta"))
        except psycopg2.Error:
            if conexao is not None:
                conexao.rollback()
            current_app.logger.exception(
                "Falha ao atualizar a conta administrativa %s.",
                current_user.id,
            )
            abort(500)
        finally:
            if conexao is not None:
                conexao.close()

        flash("Seus dados foram atualizados com sucesso.", "success")
        return redirect(url_for("admins.conta"))

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT nome, email
                FROM administradores
                WHERE id = %s
                """,
                (current_user.id,),
            )
            administrador = cursor.fetchone()
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(
            "Falha ao carregar a conta administrativa %s.",
            current_user.id,
        )
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    if administrador is None:
        abort(404)

    return render_template(
        "admins/conta.html",
        administrador={"nome": administrador[0], "email": administrador[1]},
    )


@admins.route("/home", methods=["GET"])
@login_required
def home():
    if current_user.tipo != "admin":
        abort(403)

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM usuarios WHERE ativo = TRUE),
                    (SELECT COUNT(*) FROM motoristas WHERE status = 'Ativo'),
                    (
                        SELECT COUNT(*)
                        FROM motoristas
                        WHERE status = 'Ativo' AND disponivel = TRUE
                    ),
                    (SELECT COUNT(*) FROM corridas WHERE status = 'Solicitada'),
                    (
                        SELECT COUNT(*)
                        FROM corridas
                        WHERE status IN ('Aceita', 'Em andamento')
                    ),
                    (SELECT COUNT(*) FROM pagamentos WHERE status = 'Pendente'),
                    (SELECT ROUND(AVG(nota)::numeric, 2) FROM avaliacoes)
                """
            )
            indicadores = cursor.fetchone()

            cursor.execute(
                """
                SELECT
                    c.id,
                    c.origem,
                    c.destino,
                    c.data_hora,
                    c.status,
                    c.valor,
                    u.nome,
                    m.nome
                FROM corridas AS c
                JOIN usuarios AS u ON u.id = c.id_usuario
                LEFT JOIN motoristas AS m ON m.id = c.id_motorista
                ORDER BY c.data_hora DESC, c.id DESC
                LIMIT 5
                """
            )
            corridas_recentes = [
                {
                    "id": linha[0],
                    "origem": linha[1],
                    "destino": linha[2],
                    "data_hora": linha[3],
                    "status": linha[4],
                    "valor": linha[5],
                    "usuario": linha[6],
                    "motorista": linha[7],
                }
                for linha in cursor.fetchall()
            ]
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao carregar o painel administrativo.")
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return render_template(
        "admins/home_admin.html",
        usuarios_ativos=indicadores[0],
        motoristas_ativos=indicadores[1],
        motoristas_disponiveis=indicadores[2],
        corridas_solicitadas=indicadores[3],
        corridas_ativas=indicadores[4],
        pagamentos_pendentes=indicadores[5],
        media_avaliacoes=indicadores[6],
        corridas_recentes=corridas_recentes,
    )

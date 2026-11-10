import psycopg2
from flask import Blueprint, render_template, abort, current_app
from flask_login import login_required, current_user

from conexao import criar_conexao

admins = Blueprint(
    "admins",
    __name__,
    url_prefix="/admin"
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

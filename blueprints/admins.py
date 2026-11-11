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


@admins.route("/usuarios", methods=["GET"])
@login_required
def usuarios():
    if current_user.tipo != "admin":
        abort(403)

    busca = request.args.get("busca", "").strip()
    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nome, email, telefone, ativo, data_cadastro
                FROM usuarios
                WHERE (%s = '' OR nome ILIKE %s)
                ORDER BY nome, id
                """,
                (busca, f"%{busca}%"),
            )
            usuarios_cadastrados = [
                {
                    "id": linha[0],
                    "nome": linha[1],
                    "email": linha[2],
                    "telefone": linha[3],
                    "ativo": linha[4],
                    "data_cadastro": linha[5],
                }
                for linha in cursor.fetchall()
            ]
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao carregar a lista de usuários.")
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return render_template(
        "admins/usuarios.html",
        usuarios=usuarios_cadastrados,
        busca=busca,
    )


@admins.route("/usuarios/<int:usuario_id>/status", methods=["POST"])
@login_required
def atualizar_status_usuario(usuario_id):
    if current_user.tipo != "admin":
        abort(403)

    ativo_texto = request.form.get("ativo", "")
    if ativo_texto not in ("0", "1"):
        abort(400)

    ativo = ativo_texto == "1"
    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                UPDATE usuarios
                SET ativo = %s
                WHERE id = %s
                RETURNING id
                """,
                (ativo, usuario_id),
            )
            usuario = cursor.fetchone()

        if usuario is None:
            conexao.rollback()
            abort(404)

        conexao.commit()
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(
            "Falha ao atualizar o status do usuário %s.",
            usuario_id,
        )
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    acao = "ativada" if ativo else "desativada"
    flash(f"Conta do usuário #{usuario_id} {acao}.", "success")
    busca = request.form.get("busca", "").strip()
    return redirect(url_for("admins.usuarios", busca=busca))


@admins.route("/motoristas", methods=["GET"])
@login_required
def motoristas():
    if current_user.tipo != "admin":
        abort(403)

    busca = request.args.get("busca", "").strip()
    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nome, cpf, telefone, cnh, status, disponivel
                FROM motoristas
                WHERE (%s = '' OR nome ILIKE %s)
                ORDER BY nome, id
                """,
                (busca, f"%{busca}%"),
            )
            motoristas_cadastrados = [
                {
                    "id": linha[0],
                    "nome": linha[1],
                    "cpf": linha[2],
                    "telefone": linha[3],
                    "cnh": linha[4],
                    "ativo": linha[5] == "Ativo",
                    "disponivel": linha[6],
                }
                for linha in cursor.fetchall()
            ]
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao carregar a lista de motoristas.")
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return render_template(
        "admins/motoristas.html",
        motoristas=motoristas_cadastrados,
        busca=busca,
    )


@admins.route("/motoristas/<int:motorista_id>/status", methods=["POST"])
@login_required
def atualizar_status_motorista(motorista_id):
    if current_user.tipo != "admin":
        abort(403)

    status = request.form.get("status", "")
    if status not in ("Ativo", "Inativo"):
        abort(400)

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT status
                FROM motoristas
                WHERE id = %s
                FOR UPDATE
                """,
                (motorista_id,),
            )
            motorista = cursor.fetchone()
            if motorista is None:
                conexao.rollback()
                abort(404)

            if status == "Inativo":
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM corridas
                    WHERE id_motorista = %s
                      AND status IN ('Aceita', 'Em andamento')
                    """,
                    (motorista_id,),
                )
                if cursor.fetchone()[0]:
                    conexao.rollback()
                    flash(
                        "Não é possível desativar um motorista com corridas aceitas "
                        "ou em andamento. Aguarde a conclusão ou o cancelamento.",
                        "error",
                    )
                    return redirect(url_for("admins.motoristas"))

            cursor.execute(
                """
                UPDATE motoristas
                SET status = %s::status_motorista,
                    disponivel = CASE
                        WHEN %s = 'Inativo' THEN FALSE
                        ELSE disponivel
                    END
                WHERE id = %s
                RETURNING id
                """,
                (status, status, motorista_id),
            )
            motorista = cursor.fetchone()

        if motorista is None:
            conexao.rollback()
            abort(404)

        conexao.commit()
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(
            "Falha ao atualizar o status do motorista %s.",
            motorista_id,
        )
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    acao = "ativada" if status == "Ativo" else "desativada"
    flash(f"Conta do motorista #{motorista_id} {acao}.", "success")
    busca = request.form.get("busca", "").strip()
    return redirect(url_for("admins.motoristas", busca=busca))


@admins.route("/corridas", methods=["GET"])
@login_required
def corridas():
    if current_user.tipo != "admin":
        abort(403)

    status_filtro = request.args.get("status", "").strip()
    status_validos = (
        "Solicitada",
        "Aceita",
        "Em andamento",
        "Finalizada",
        "Cancelada",
    )
    if status_filtro and status_filtro not in status_validos:
        abort(400)

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
                    u.nome,
                    m.nome,
                    p.forma_pagamento,
                    p.status,
                    p.valor,
                    a.nota,
                    a.comentario,
                    h.id,
                    h.status_anterior,
                    h.novo_status,
                    h.data_alteracao
                FROM corridas AS c
                JOIN usuarios AS u ON u.id = c.id_usuario
                LEFT JOIN motoristas AS m ON m.id = c.id_motorista
                LEFT JOIN pagamentos AS p ON p.id_corrida = c.id
                LEFT JOIN avaliacoes AS a ON a.id_corrida = c.id
                LEFT JOIN historico_corridas AS h ON h.id_corrida = c.id
                WHERE (%s = '' OR c.status::text = %s)
                ORDER BY c.data_hora DESC, c.id DESC, h.data_alteracao, h.id
                """,
                (status_filtro, status_filtro),
            )

            corridas_por_id = {}
            for linha in cursor.fetchall():
                corrida = corridas_por_id.get(linha[0])
                if corrida is None:
                    corrida = {
                        "id": linha[0],
                        "origem": linha[1],
                        "destino": linha[2],
                        "data_hora": linha[3],
                        "status": linha[4],
                        "distancia_km": linha[5],
                        "valor": linha[6],
                        "usuario": linha[7],
                        "motorista": linha[8],
                        "pagamento": (
                            {
                                "forma": linha[9],
                                "status": linha[10],
                                "valor": linha[11],
                            }
                            if linha[9] is not None
                            else None
                        ),
                        "avaliacao": (
                            {"nota": linha[12], "comentario": linha[13]}
                            if linha[12] is not None
                            else None
                        ),
                        "historico": [],
                    }
                    corridas_por_id[linha[0]] = corrida

                if linha[14] is not None:
                    corrida["historico"].append(
                        {
                            "status_anterior": linha[15],
                            "novo_status": linha[16],
                            "data_alteracao": linha[17],
                        }
                    )

    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao carregar o histórico administrativo de corridas.")
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return render_template(
        "admins/corridas.html",
        corridas=list(corridas_por_id.values()),
        status_filtro=status_filtro,
        status_validos=status_validos,
    )


@admins.route("/pagamentos", methods=["GET"])
@login_required
def pagamentos():
    if current_user.tipo != "admin":
        abort(403)

    status_filtro = request.args.get("status", "").strip()
    forma_filtro = request.args.get("forma", "").strip()
    status_validos = ("Pendente", "Pago", "Cancelado")
    formas_validas = ("Pix", "Dinheiro", "Cartão")

    if status_filtro and status_filtro not in status_validos:
        abort(400)
    if forma_filtro and forma_filtro not in formas_validas:
        abort(400)

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(*) FILTER (WHERE status = 'Pendente'),
                    COALESCE(SUM(valor) FILTER (WHERE status = 'Pendente'), 0),
                    COUNT(*) FILTER (WHERE status = 'Pago'),
                    COALESCE(SUM(valor) FILTER (WHERE status = 'Pago'), 0),
                    COUNT(*)
                FROM pagamentos
                """
            )
            resumo = cursor.fetchone()

            cursor.execute(
                """
                SELECT
                    p.id,
                    p.id_corrida,
                    p.forma_pagamento,
                    p.valor,
                    p.status,
                    p.data_pagamento,
                    c.origem,
                    c.destino,
                    c.data_hora,
                    c.status,
                    u.nome,
                    m.nome
                FROM pagamentos AS p
                JOIN corridas AS c ON c.id = p.id_corrida
                JOIN usuarios AS u ON u.id = c.id_usuario
                LEFT JOIN motoristas AS m ON m.id = c.id_motorista
                WHERE (%s = '' OR p.status::text = %s)
                  AND (%s = '' OR p.forma_pagamento::text = %s)
                ORDER BY p.data_pagamento DESC, p.id DESC
                """,
                (status_filtro, status_filtro, forma_filtro, forma_filtro),
            )
            pagamentos_registrados = [
                {
                    "id": linha[0],
                    "corrida_id": linha[1],
                    "forma": linha[2],
                    "valor": linha[3],
                    "status": linha[4],
                    "data_registro": linha[5],
                    "origem": linha[6],
                    "destino": linha[7],
                    "data_corrida": linha[8],
                    "status_corrida": linha[9],
                    "usuario": linha[10],
                    "motorista": linha[11],
                }
                for linha in cursor.fetchall()
            ]
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao carregar o painel administrativo de pagamentos.")
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return render_template(
        "admins/pagamentos.html",
        pagamentos=pagamentos_registrados,
        total_pendentes=resumo[0],
        valor_pendente=resumo[1],
        total_pagos=resumo[2],
        valor_pago=resumo[3],
        total_pagamentos=resumo[4],
        status_filtro=status_filtro,
        forma_filtro=forma_filtro,
        status_validos=status_validos,
        formas_validas=formas_validas,
    )


@admins.route("/avaliacoes", methods=["GET"])
@login_required
def avaliacoes():
    if current_user.tipo != "admin":
        abort(403)

    nota_texto = request.args.get("nota", "").strip()
    if nota_texto and nota_texto not in {"1", "2", "3", "4", "5"}:
        abort(400)

    nota_filtro = int(nota_texto) if nota_texto else None
    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*), ROUND(AVG(nota)::numeric, 2)
                FROM avaliacoes
                """
            )
            resumo = cursor.fetchone()

            cursor.execute(
                """
                SELECT
                    a.id,
                    a.id_corrida,
                    a.nota,
                    a.comentario,
                    a.data_avaliacao,
                    u.nome,
                    m.nome,
                    c.origem,
                    c.destino,
                    c.status
                FROM avaliacoes AS a
                JOIN corridas AS c ON c.id = a.id_corrida
                JOIN usuarios AS u ON u.id = c.id_usuario
                LEFT JOIN motoristas AS m ON m.id = c.id_motorista
                WHERE (%s IS NULL OR a.nota = %s)
                ORDER BY a.data_avaliacao DESC, a.id DESC
                """,
                (nota_filtro, nota_filtro),
            )
            avaliacoes_registradas = [
                {
                    "id": linha[0],
                    "corrida_id": linha[1],
                    "nota": linha[2],
                    "comentario": linha[3],
                    "data_avaliacao": linha[4],
                    "usuario": linha[5],
                    "motorista": linha[6],
                    "origem": linha[7],
                    "destino": linha[8],
                    "status_corrida": linha[9],
                }
                for linha in cursor.fetchall()
            ]
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao carregar as avaliações administrativas.")
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return render_template(
        "admins/avaliacoes.html",
        avaliacoes=avaliacoes_registradas,
        total_avaliacoes=resumo[0],
        media_avaliacoes=resumo[1],
        nota_filtro=nota_texto,
        notas_validas=range(1, 6),
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

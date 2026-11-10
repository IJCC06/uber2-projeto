from decimal import Decimal, InvalidOperation

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

motoristas = Blueprint(
    "motoristas",
    __name__,
    url_prefix="/motorista"
)

TARIFA_POR_KM = Decimal("2.50")


def _ler_dados_veiculo():
    modelo = request.form.get("modelo", "").strip()
    marca = request.form.get("marca", "").strip()
    placa = request.form.get("placa", "").strip().upper()
    ano_texto = request.form.get("ano", "").strip()
    cor = request.form.get("cor", "").strip() or None

    erros = []
    if not modelo or len(modelo) > 50:
        erros.append("Informe um modelo com até 50 caracteres.")
    if not marca or len(marca) > 50:
        erros.append("Informe uma marca com até 50 caracteres.")
    if not placa or len(placa) > 10:
        erros.append("Informe uma placa com até 10 caracteres.")
    if cor is not None and len(cor) > 30:
        erros.append("A cor deve ter até 30 caracteres.")

    try:
        ano = int(ano_texto)
        if ano <= 0:
            raise ValueError
    except ValueError:
        ano = None
        erros.append("Informe um ano válido.")

    return (modelo, marca, placa, ano, cor), erros


@motoristas.route("/home", methods=["GET"])
@login_required
def home():
    if current_user.tipo != "motorista":
        abort(403)

    return render_template("motoristas/home_motorista.html")


@motoristas.route("/corridas-disponiveis", methods=["GET"])
@login_required
def corridas_disponiveis():
    if current_user.tipo != "motorista":
        abort(403)

    conexao = criar_conexao()

    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT status, disponivel
                FROM motoristas
                WHERE id = %s
                """,
                (current_user.id,),
            )
            motorista = cursor.fetchone()

            if motorista is None:
                abort(403)

            motorista_ativo = motorista[0] == "Ativo"
            disponivel = motorista[1]
            pode_receber = motorista_ativo and disponivel

            cursor.execute(
                """
                SELECT COUNT(a.id), ROUND(AVG(a.nota)::numeric, 2)
                FROM avaliacoes AS a
                JOIN corridas AS c ON c.id = a.id_corrida
                WHERE c.id_motorista = %s
                """,
                (current_user.id,),
            )
            resumo_avaliacoes = cursor.fetchone()

            cursor.execute(
                """
                SELECT
                    a.nota,
                    a.comentario,
                    a.data_avaliacao,
                    c.id,
                    u.nome
                FROM avaliacoes AS a
                JOIN corridas AS c ON c.id = a.id_corrida
                JOIN usuarios AS u ON u.id = c.id_usuario
                WHERE c.id_motorista = %s
                ORDER BY a.data_avaliacao DESC, a.id DESC
                LIMIT 5
                """,
                (current_user.id,),
            )
            avaliacoes_recentes = [
                {
                    "nota": linha[0],
                    "comentario": linha[1],
                    "data": linha[2],
                    "corrida_id": linha[3],
                    "usuario": linha[4],
                }
                for linha in cursor.fetchall()
            ]

            corridas = []

            if pode_receber:
                cursor.execute(
                    """
                    SELECT c.id, u.nome, c.origem, c.destino, c.data_hora
                    FROM corridas AS c
                    JOIN usuarios AS u ON u.id = c.id_usuario
                    WHERE c.status = 'Solicitada'
                      AND c.id_motorista IS NULL
                    ORDER BY c.data_hora
                    """
                )

                corridas = [
                    {
                        "id": linha[0],
                        "usuario": linha[1],
                        "origem": linha[2],
                        "destino": linha[3],
                        "data_hora": linha[4],
                    }
                    for linha in cursor.fetchall()
                ]

            cursor.execute(
                """
                SELECT c.id, u.nome, c.origem, c.destino, c.data_hora, c.status
                FROM corridas AS c
                JOIN usuarios AS u ON u.id = c.id_usuario
                WHERE c.id_motorista = %s
                  AND c.status IN ('Aceita', 'Em andamento')
                ORDER BY c.data_hora
                """,
                (current_user.id,),
            )
            corridas_ativas = [
                {
                    "id": linha[0],
                    "usuario": linha[1],
                    "origem": linha[2],
                    "destino": linha[3],
                    "data_hora": linha[4],
                    "status": linha[5],
                }
                for linha in cursor.fetchall()
            ]
    finally:
        conexao.close()

    return render_template(
        "motoristas/home_motorista.html",
        corridas_disponiveis=corridas,
        corridas_ativas=corridas_ativas,
        motorista_ativo=motorista_ativo,
        disponivel=disponivel,
        pode_receber=pode_receber,
        quantidade_avaliacoes=resumo_avaliacoes[0],
        media_avaliacoes=resumo_avaliacoes[1],
        avaliacoes_recentes=avaliacoes_recentes,
    )


@motoristas.route("/disponibilidade", methods=["POST"])
@login_required
def atualizar_disponibilidade():
    if current_user.tipo != "motorista":
        abort(403)

    valor_disponibilidade = request.form.get("disponivel")
    if valor_disponibilidade not in {"0", "1"}:
        flash("Solicitação de disponibilidade inválida.", "error")
        return redirect(url_for("motoristas.corridas_disponiveis"))

    disponivel = valor_disponibilidade == "1"
    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                UPDATE motoristas
                SET disponivel = %s
                WHERE id = %s
                  AND (status = 'Ativo' OR %s = FALSE)
                RETURNING disponivel
                """,
                (disponivel, current_user.id, disponivel),
            )
            resultado = cursor.fetchone()

        if resultado is None:
            conexao.rollback()
            flash(
                "Sua conta precisa estar ativa para habilitar o recebimento de corridas.",
                "error",
            )
        else:
            conexao.commit()
            mensagem = (
                "Você está disponível para receber corridas."
                if resultado[0]
                else "Você não receberá novas solicitações de corrida."
            )
            flash(mensagem, "success")
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(
            "Falha ao atualizar a disponibilidade do motorista %s.",
            current_user.id,
        )
        flash("Não foi possível atualizar sua disponibilidade. Tente novamente.", "error")
    finally:
        if conexao is not None:
            conexao.close()

    return redirect(url_for("motoristas.corridas_disponiveis"))


@motoristas.route("/veiculos", methods=["GET", "POST"])
@login_required
def meus_veiculos():
    if current_user.tipo != "motorista":
        abort(403)

    if request.method == "POST":
        dados_veiculo, erros = _ler_dados_veiculo()
        if erros:
            for erro in erros:
                flash(erro, "error")
            return redirect(url_for("motoristas.meus_veiculos"))

        modelo, marca, placa, ano, cor = dados_veiculo
        conexao = None
        try:
            conexao = criar_conexao()
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO veiculos
                        (id_motorista, modelo, marca, placa, ano, cor)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (current_user.id, modelo, marca, placa, ano, cor),
                )
            conexao.commit()
        except psycopg2.errors.UniqueViolation:
            if conexao is not None:
                conexao.rollback()
            flash("Já existe um veículo cadastrado com essa placa.", "error")
            return redirect(url_for("motoristas.meus_veiculos"))
        except psycopg2.Error:
            if conexao is not None:
                conexao.rollback()
            current_app.logger.exception(
                "Falha ao cadastrar veículo para o motorista %s.",
                current_user.id,
            )
            abort(500)
        finally:
            if conexao is not None:
                conexao.close()

        flash("Veículo cadastrado com sucesso.", "success")
        return redirect(url_for("motoristas.meus_veiculos"))

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, modelo, marca, placa, ano, cor
                FROM veiculos
                WHERE id_motorista = %s
                ORDER BY id DESC
                """,
                (current_user.id,),
            )
            veiculos = [
                {
                    "id": linha[0],
                    "modelo": linha[1],
                    "marca": linha[2],
                    "placa": linha[3],
                    "ano": linha[4],
                    "cor": linha[5],
                }
                for linha in cursor.fetchall()
            ]
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(
            "Falha ao carregar os veículos do motorista %s.",
            current_user.id,
        )
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return render_template("motoristas/meus_veiculos.html", veiculos=veiculos)


@motoristas.route("/veiculos/<int:veiculo_id>/editar", methods=["POST"])
@login_required
def editar_veiculo(veiculo_id):
    if current_user.tipo != "motorista":
        abort(403)

    dados_veiculo, erros = _ler_dados_veiculo()
    if erros:
        for erro in erros:
            flash(erro, "error")
        return redirect(url_for("motoristas.meus_veiculos"))

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                UPDATE veiculos
                SET modelo = %s,
                    marca = %s,
                    placa = %s,
                    ano = %s,
                    cor = %s
                WHERE id = %s
                  AND id_motorista = %s
                RETURNING id
                """,
                (*dados_veiculo, veiculo_id, current_user.id),
            )
            veiculo = cursor.fetchone()

        if veiculo is None:
            conexao.rollback()
            flash("Veículo não encontrado na sua conta.", "error")
        else:
            conexao.commit()
            flash("Veículo atualizado com sucesso.", "success")
    except psycopg2.errors.UniqueViolation:
        if conexao is not None:
            conexao.rollback()
        flash("Já existe um veículo cadastrado com essa placa.", "error")
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(
            "Falha ao atualizar o veículo %s do motorista %s.",
            veiculo_id,
            current_user.id,
        )
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return redirect(url_for("motoristas.meus_veiculos"))


@motoristas.route("/veiculos/<int:veiculo_id>/excluir", methods=["POST"])
@login_required
def excluir_veiculo(veiculo_id):
    if current_user.tipo != "motorista":
        abort(403)

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM veiculos
                WHERE id = %s
                  AND id_motorista = %s
                RETURNING id
                """,
                (veiculo_id, current_user.id),
            )
            veiculo = cursor.fetchone()

        if veiculo is None:
            conexao.rollback()
            flash("Veículo não encontrado na sua conta.", "error")
        else:
            conexao.commit()
            flash("Veículo excluído com sucesso.", "success")
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(
            "Falha ao excluir o veículo %s do motorista %s.",
            veiculo_id,
            current_user.id,
        )
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()

    return redirect(url_for("motoristas.meus_veiculos"))


@motoristas.route("/corridas/<int:corrida_id>/aceitar", methods=["POST"])
@login_required
def aceitar_corrida(corrida_id):
    if current_user.tipo != "motorista":
        abort(403)

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT status, disponivel
                FROM motoristas
                WHERE id = %s
                FOR UPDATE
                """,
                (current_user.id,),
            )
            motorista = cursor.fetchone()

            if motorista is None or motorista[0] != "Ativo" or not motorista[1]:
                conexao.rollback()
                flash("Sua conta precisa estar ativa e disponível para aceitar corridas.", "error")
                return redirect(url_for("motoristas.corridas_disponiveis"))
            cursor.execute(
                """
                UPDATE corridas
                SET id_motorista = %s,
                    status = 'Aceita'
                WHERE id = %s
                  AND status = 'Solicitada'
                  AND id_motorista IS NULL
                """,
                (current_user.id, corrida_id),
            )

            if cursor.rowcount == 0:
                conexao.rollback()
                flash("Esta corrida não está mais disponível.", "error")
                return redirect(url_for("motoristas.corridas_disponiveis"))

            cursor.execute(
                """
                INSERT INTO historico_corridas
                    (id_corrida, status_anterior, novo_status)
                VALUES (%s, 'Solicitada', 'Aceita')
                """,
                (corrida_id,),
            )

        conexao.commit()
        flash(f"Corrida #{corrida_id} aceita com sucesso.", "success")
        return redirect(url_for("motoristas.corridas_disponiveis"))
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao aceitar a corrida %s.", corrida_id)
        flash("Não foi possível aceitar a corrida. Tente novamente.", "error")
    finally:
        if conexao is not None:
            conexao.close()

    return redirect(url_for("motoristas.corridas_disponiveis"))


@motoristas.route("/corridas/<int:corrida_id>/iniciar", methods=["POST"])
@login_required
def iniciar_corrida(corrida_id):
    if current_user.tipo != "motorista":
        abort(403)

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                UPDATE corridas
                SET status = 'Em andamento'
                WHERE id = %s
                  AND id_motorista = %s
                  AND status = 'Aceita'
                """,
                (corrida_id, current_user.id),
            )

            if cursor.rowcount == 0:
                conexao.rollback()
                flash(
                    "Esta corrida não está mais disponível para iniciar.",
                    "error",
                )
                return redirect(url_for("motoristas.corridas_disponiveis"))

            cursor.execute(
                """
                INSERT INTO historico_corridas
                    (id_corrida, status_anterior, novo_status)
                VALUES (%s, 'Aceita', 'Em andamento')
                """,
                (corrida_id,),
            )

        conexao.commit()
        flash(f"Corrida #{corrida_id} iniciada.", "success")
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao iniciar a corrida %s.", corrida_id)
        flash("Não foi possível iniciar a corrida. Tente novamente.", "error")
    finally:
        if conexao is not None:
            conexao.close()

    return redirect(url_for("motoristas.corridas_disponiveis"))


@motoristas.route("/corridas/<int:corrida_id>/cancelar", methods=["POST"])
@login_required
def cancelar_corrida(corrida_id):
    if current_user.tipo != "motorista":
        abort(403)

    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT status
                FROM corridas
                WHERE id = %s
                  AND id_motorista = %s
                FOR UPDATE
                """,
                (corrida_id, current_user.id),
            )
            corrida = cursor.fetchone()

            if corrida is None or corrida[0] not in ("Aceita", "Em andamento"):
                conexao.rollback()
                flash("Esta corrida não pode mais ser cancelada.", "error")
                return redirect(url_for("motoristas.corridas_disponiveis"))

            status_anterior = corrida[0]
            cursor.execute(
                """
                UPDATE corridas
                SET status = 'Cancelada'
                WHERE id = %s
                  AND id_motorista = %s
                  AND status = %s
                """,
                (corrida_id, current_user.id, status_anterior),
            )

            if cursor.rowcount == 0:
                conexao.rollback()
                flash("Esta corrida não pode mais ser cancelada.", "error")
                return redirect(url_for("motoristas.corridas_disponiveis"))

            cursor.execute(
                """
                INSERT INTO historico_corridas
                    (id_corrida, status_anterior, novo_status)
                VALUES (%s, %s, 'Cancelada')
                """,
                (corrida_id, status_anterior),
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

    return redirect(url_for("motoristas.corridas_disponiveis"))


@motoristas.route("/corridas/<int:corrida_id>/finalizar", methods=["POST"])
@login_required
def finalizar_corrida(corrida_id):
    if current_user.tipo != "motorista":
        abort(403)

    distancia_texto = request.form.get("distancia_km", "").strip().replace(",", ".")
    try:
        distancia_km = Decimal(distancia_texto)
    except InvalidOperation:
        flash("Informe uma distância válida em quilômetros.", "error")
        return redirect(url_for("motoristas.corridas_disponiveis"))

    if (
        not distancia_km.is_finite()
        or distancia_km <= 0
        or distancia_km > Decimal("999999.99")
        or distancia_km != distancia_km.quantize(Decimal("0.01"))
    ):
        flash(
            "A distância deve ser positiva e ter no máximo duas casas decimais.",
            "error",
        )
        return redirect(url_for("motoristas.corridas_disponiveis"))

    valor = (distancia_km * TARIFA_POR_KM).quantize(Decimal("0.01"))
    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                UPDATE corridas
                SET status = 'Finalizada',
                    distancia_km = %s,
                    valor = %s
                WHERE id = %s
                  AND id_motorista = %s
                  AND status = 'Em andamento'
                """,
                (distancia_km, valor, corrida_id, current_user.id),
            )

            if cursor.rowcount == 0:
                conexao.rollback()
                flash(
                    "Esta corrida não está mais disponível para finalizar.",
                    "error",
                )
                return redirect(url_for("motoristas.corridas_disponiveis"))

            cursor.execute(
                """
                INSERT INTO historico_corridas
                    (id_corrida, status_anterior, novo_status)
                VALUES (%s, 'Em andamento', 'Finalizada')
                """,
                (corrida_id,),
            )

        conexao.commit()
        flash(
            f"Corrida #{corrida_id} finalizada. Distância: {distancia_km:.2f} km; "
            f"valor: R$ {valor:.2f}.",
            "success",
        )
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception("Falha ao finalizar a corrida %s.", corrida_id)
        flash("Não foi possível finalizar a corrida. Tente novamente.", "error")
    finally:
        if conexao is not None:
            conexao.close()

    return redirect(url_for("motoristas.corridas_disponiveis"))

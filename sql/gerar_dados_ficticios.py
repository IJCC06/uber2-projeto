"""Insere dados ficticios de desenvolvimento no banco configurado no .env."""

import os
import string
import uuid
from datetime import timedelta
from decimal import Decimal

import psycopg
from dotenv import load_dotenv
from faker import Faker
from werkzeug.security import generate_password_hash


load_dotenv()

fake = Faker("pt_BR")
SENHA_TESTE = "Teste123!"
QUANTIDADE_USUARIOS = 20
QUANTIDADE_MOTORISTAS = 12
QUANTIDADE_CORRIDAS = 60


def valor_unico(valores_existentes, gerador):
    while True:
        valor = gerador()
        if valor not in valores_existentes:
            valores_existentes.add(valor)
            return valor


def gerar_cpf():
    digitos = "".join(str(fake.random_int(0, 9)) for _ in range(11))
    return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"


def gerar_placa():
    letras = "".join(fake.random_choices(string.ascii_uppercase, length=3))
    numeros = fake.random_number(digits=4, fix_len=True)
    return f"{letras}-{numeros}"


def registrar_historico(cursor, corrida_id, status, data_hora):
    transicoes = {
        "Aceita": [("Solicitada", "Aceita", 0)],
        "Em andamento": [
            ("Solicitada", "Aceita", 0),
            ("Aceita", "Em andamento", 5),
        ],
        "Finalizada": [
            ("Solicitada", "Aceita", 0),
            ("Aceita", "Em andamento", 5),
            ("Em andamento", "Finalizada", 25),
        ],
        "Cancelada": [("Solicitada", "Cancelada", 0)],
    }

    for anterior, novo, minutos in transicoes.get(status, []):
        cursor.execute(
            """
            INSERT INTO historico_corridas
                (id_corrida, status_anterior, novo_status, data_alteracao)
            VALUES (%s, %s, %s, %s)
            """,
            (corrida_id, anterior, novo, data_hora + timedelta(minutes=minutos)),
        )


def main():
    nomes_variaveis = ("DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD")
    configuracao = {nome: os.getenv(nome) for nome in nomes_variaveis}
    ausentes = [nome for nome, valor in configuracao.items() if not valor]
    if ausentes:
        raise RuntimeError(
            "Configure no .env as variaveis: " + ", ".join(ausentes)
        )

    senha_hash = generate_password_hash(SENHA_TESTE)
    with psycopg.connect(
        host=configuracao["DB_HOST"],
        dbname=configuracao["DB_NAME"],
        user=configuracao["DB_USER"],
        password=configuracao["DB_PASSWORD"],
    ) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT email FROM usuarios")
            emails_existentes = {linha[0] for linha in cursor.fetchall()}
            cursor.execute("SELECT email FROM administradores")
            emails_existentes.update(linha[0] for linha in cursor.fetchall())
            cursor.execute("SELECT cpf, cnh FROM motoristas")
            documentos_existentes = {valor for linha in cursor.fetchall() for valor in linha}
            cursor.execute("SELECT placa FROM veiculos")
            placas_existentes = {linha[0] for linha in cursor.fetchall()}

            email_admin = valor_unico(
                emails_existentes,
                lambda: f"admin.{uuid.uuid4().hex[:10]}@example.test",
            )
            cursor.execute(
                """
                INSERT INTO administradores (nome, email, senha, ativo)
                VALUES (%s, %s, %s, TRUE)
                """,
                ("Administrador de Teste", email_admin, senha_hash),
            )

            usuarios_ids = []
            for indice in range(QUANTIDADE_USUARIOS):
                email = valor_unico(
                    emails_existentes,
                    lambda: f"{fake.user_name()}.{uuid.uuid4().hex[:8]}@example.test",
                )
                cursor.execute(
                    """
                    INSERT INTO usuarios (nome, email, telefone, senha, ativo)
                    VALUES (%s, %s, %s, %s, TRUE)
                    RETURNING id
                    """,
                    (fake.name()[:100], email, fake.phone_number()[:20], senha_hash),
                )
                usuarios_ids.append(cursor.fetchone()[0])

            motoristas_ids = []
            motoristas_ativos = []
            for indice in range(QUANTIDADE_MOTORISTAS):
                cpf = valor_unico(documentos_existentes, gerar_cpf)
                cnh = valor_unico(
                    documentos_existentes,
                    lambda: "".join(
                        str(fake.random_int(0, 9)) for _ in range(11)
                    ),
                )
                status = "Ativo" if indice < 9 else "Inativo"
                disponivel = status == "Ativo" and fake.boolean(chance_of_getting_true=60)

                cursor.execute(
                    """
                    INSERT INTO motoristas
                        (nome, cpf, telefone, cnh, senha, status, disponivel)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        fake.name()[:100],
                        cpf,
                        fake.phone_number()[:20],
                        cnh,
                        senha_hash,
                        status,
                        disponivel,
                    ),
                )
                motorista_id = cursor.fetchone()[0]
                motoristas_ids.append(motorista_id)
                if status == "Ativo":
                    motoristas_ativos.append(motorista_id)

                placa = valor_unico(placas_existentes, gerar_placa)
                cursor.execute(
                    """
                    INSERT INTO veiculos
                        (id_motorista, modelo, marca, placa, ano, cor)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        motorista_id,
                        fake.word().title()[:50],
                        fake.company()[:50],
                        placa,
                        fake.random_int(min=2015, max=2026),
                        fake.color_name()[:30],
                    ),
                )

            status_corridas = (
                ["Finalizada"] * 24
                + ["Em andamento"] * 8
                + ["Aceita"] * 8
                + ["Solicitada"] * 10
                + ["Cancelada"] * 10
            )
            fake.random.shuffle(status_corridas)

            for indice, status in enumerate(status_corridas):
                origem = fake.street_address()[:100]
                destino = fake.street_address()[:100]
                while origem.strip().casefold() == destino.strip().casefold():
                    destino = fake.street_address()[:100]

                motorista_id = None
                if status != "Solicitada":
                    opcoes = (
                        motoristas_ativos
                        if status in ("Aceita", "Em andamento")
                        else motoristas_ids
                    )
                    motorista_id = fake.random_element(opcoes)

                data_hora = fake.date_time_between(start_date="-120d", end_date="now")
                distancia_km = None
                valor = None
                if status == "Finalizada":
                    distancia_km = fake.pydecimal(
                        left_digits=2,
                        right_digits=2,
                        positive=True,
                    )
                    valor = (distancia_km * Decimal("2.50")).quantize(
                        Decimal("0.01")
                    )
                usuario_id = usuarios_ids[indice % len(usuarios_ids)]

                cursor.execute(
                    """
                    INSERT INTO corridas
                        (
                            id_usuario,
                            id_motorista,
                            origem,
                            destino,
                            data_hora,
                            distancia_km,
                            valor,
                            status
                        )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        usuario_id,
                        motorista_id,
                        origem,
                        destino,
                        data_hora,
                        distancia_km,
                        valor,
                        status,
                    ),
                )
                corrida_id = cursor.fetchone()[0]
                registrar_historico(cursor, corrida_id, status, data_hora)

                if status == "Finalizada":
                    cursor.execute(
                        """
                        INSERT INTO pagamentos
                            (id_corrida, forma_pagamento, valor, status, data_pagamento)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            corrida_id,
                            fake.random_element(("Pix", "Dinheiro", "Cartão")),
                            valor,
                            fake.random_element(("Pago", "Pendente")),
                            data_hora + timedelta(minutes=30),
                        ),
                    )

                    if fake.boolean(chance_of_getting_true=80):
                        cursor.execute(
                            """
                            INSERT INTO avaliacoes
                                (id_corrida, nota, comentario, data_avaliacao)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                corrida_id,
                                fake.random_int(min=1, max=5),
                                fake.text(max_nb_chars=100),
                                data_hora + timedelta(hours=1),
                            ),
                        )

    print("Dados ficticios inseridos com sucesso.")
    print(f"Login de administrador: {email_admin}")
    print(f"Senha de teste para todas as contas: {SENHA_TESTE}")
    print("Os CPFs e demais dados pessoais gerados sao ficticios.")


if __name__ == "__main__":
    main()

import os
import unittest
import uuid
from decimal import Decimal
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from werkzeug.security import generate_password_hash


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

import app as app_module
import blueprints.admins as admins_module
import blueprints.auth as auth_module
import blueprints.motoristas as motoristas_module
import blueprints.usuarios as usuarios_module
import python.logins as logins_module


class PostgresAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.getenv("UBER2_TEST_POSTGRES") != "1":
            raise unittest.SkipTest(
                "Set UBER2_TEST_POSTGRES=1 to run against an isolated PostgreSQL schema."
            )

        cls.db_config = {
            "host": os.getenv("DB_HOST"),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "connect_timeout": 5,
        }
        missing = [key for key, value in cls.db_config.items() if not value]
        if missing:
            raise unittest.SkipTest(
                "Missing PostgreSQL settings: " + ", ".join(missing)
            )

        cls.schema = f"uber2_acceptance_{uuid.uuid4().hex}"
        connection = psycopg2.connect(**cls.db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(cls.schema))
                )
            connection.commit()
        finally:
            connection.close()

        try:
            schema_connection = cls.database_connection()
            try:
                schema_sql = (ROOT / "sql" / "create-table.sql").read_text(
                    encoding="utf-8"
                )
                with schema_connection.cursor() as cursor:
                    cursor.execute(schema_sql)
                schema_connection.commit()
            except Exception:
                schema_connection.rollback()
                raise
            finally:
                schema_connection.close()
        except Exception:
            connection = psycopg2.connect(**cls.db_config)
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        sql.SQL("DROP SCHEMA {} CASCADE").format(
                            sql.Identifier(cls.schema)
                        )
                    )
                connection.commit()
            finally:
                connection.close()
            raise

        cls.modules = (
            app_module,
            admins_module,
            auth_module,
            motoristas_module,
            usuarios_module,
            logins_module,
        )
        cls.original_factories = {
            module: module.criar_conexao for module in cls.modules
        }
        for module in cls.modules:
            module.criar_conexao = cls.database_connection

        cls.app = app_module.uber2
        cls.original_testing = cls.app.config["TESTING"]
        cls.app.config.update(TESTING=True)

    @classmethod
    def tearDownClass(cls):
        for module, factory in getattr(cls, "original_factories", {}).items():
            module.criar_conexao = factory
        if hasattr(cls, "original_testing"):
            cls.app.config["TESTING"] = cls.original_testing

        if not hasattr(cls, "schema"):
            return

        connection = psycopg2.connect(**cls.db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    sql.SQL("DROP SCHEMA {} CASCADE").format(
                        sql.Identifier(cls.schema)
                    )
                )
            connection.commit()
        finally:
            connection.close()

    @classmethod
    def database_connection(cls):
        return psycopg2.connect(
            **cls.db_config,
            options=f"-c search_path={cls.schema}",
        )

    def setUp(self):
        connection = self.database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    TRUNCATE TABLE
                        historico_corridas,
                        avaliacoes,
                        pagamentos,
                        corridas,
                        veiculos,
                        motoristas,
                        usuarios,
                        administradores
                    RESTART IDENTITY CASCADE
                    """
                )
                cursor.execute(
                    """
                    INSERT INTO administradores (nome, email, senha, ativo)
                    VALUES (%s, %s, %s, TRUE)
                    """,
                    (
                        "Administrador de Teste",
                        "admin@example.test",
                        generate_password_hash("senha-admin-teste"),
                    ),
                )
            connection.commit()
        finally:
            connection.close()

    def login_admin(self):
        client = self.app.test_client()
        response = client.post(
            "/login/admin",
            data={"email": "admin@example.test", "password": "senha-admin-teste"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/admin/home"))
        return client

    def test_complete_registration_and_ride_acceptance_flow(self):
        user_client = self.app.test_client()
        response = user_client.post(
            "/cadastro",
            data={
                "nome": "Usuária de Teste",
                "email": "usuario@example.test",
                "telefone": "11999990000",
                "senha": "senha-usuario-teste",
                "confirmar_senha": "senha-usuario-teste",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cadastro realizado com sucesso", response.data)

        driver_registration_client = self.app.test_client()
        response = driver_registration_client.post(
            "/cadastro/motorista",
            data={
                "nome": "Motorista de Teste",
                "cpf": "123.456.789-00",
                "telefone": "11999990001",
                "cnh": "12345678901",
                "senha": "senha-motorista-teste",
                "confirmar_senha": "senha-motorista-teste",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ficar\xc3\xa1 inativa", response.data)

        connection = self.database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, ativo FROM usuarios WHERE email = %s",
                    ("usuario@example.test",),
                )
                user_id, user_active = cursor.fetchone()
                self.assertTrue(user_active)

                cursor.execute(
                    "SELECT id, status, disponivel FROM motoristas WHERE cpf = %s",
                    ("123.456.789-00",),
                )
                driver_id, driver_status, driver_available = cursor.fetchone()
                self.assertEqual(driver_status, "Inativo")
                self.assertFalse(driver_available)
        finally:
            connection.close()

        response = driver_registration_client.post(
            "/login/motorista",
            data={"cpf": "123.456.789-00", "password": "senha-motorista-teste"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CPF ou senha inv\xc3\xa1lidos", response.data)

        admin_client = self.login_admin()
        for path, search_term, included_name, excluded_name in (
            (
                "/admin/usuarios",
                "USUÁRIA",
                "Usuária de Teste",
                "Motorista de Teste",
            ),
            (
                "/admin/motoristas",
                "motorista de",
                "Motorista de Teste",
                "Usuária de Teste",
            ),
        ):
            with self.subTest(name_search=path):
                response = admin_client.get(
                    path,
                    query_string={"busca": search_term},
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn(included_name.encode("utf-8"), response.data)
                self.assertNotIn(excluded_name.encode("utf-8"), response.data)

                response = admin_client.get(
                    path,
                    query_string={"busca": "nome inexistente"},
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"Nenhum ", response.data)
                self.assertIn(b"encontrado", response.data)

        response = admin_client.post(
            f"/admin/motoristas/{driver_id}/status",
            data={"status": "Ativo", "busca": "motorista de"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("busca=motorista+de", response.headers["Location"])

        driver_client = self.app.test_client()
        response = driver_client.post(
            "/login/motorista",
            data={"cpf": "123.456.789-00", "password": "senha-motorista-teste"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/motorista/home"))

        response = user_client.post(
            "/login/usuario",
            data={
                "email": "usuario@example.test",
                "password": "senha-usuario-teste",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/usuario/home"))

        response = user_client.post(
            "/usuario/corridas/solicitar",
            data={"origem": "Rua Um, 10", "destino": "Rua Um, 10"},
        )
        self.assertEqual(response.status_code, 400)
        invalid_requests = (
            {"origem": "", "destino": "Avenida Dois, 20"},
            {"origem": "x" * 101, "destino": "Avenida Dois, 20"},
            {"origem": " Rua Um, 10 ", "destino": "rua um, 10"},
        )
        for request_data in invalid_requests:
            with self.subTest(invalid_ride_request=request_data):
                response = user_client.post(
                    "/usuario/corridas/solicitar",
                    data=request_data,
                )
                self.assertEqual(response.status_code, 400)

        response = user_client.post(
            "/usuario/corridas/solicitar",
            data={"origem": "Rua Um, 10", "destino": "Avenida Dois, 20"},
        )
        self.assertEqual(response.status_code, 302)

        connection = self.database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM corridas WHERE id_usuario = %s",
                    (user_id,),
                )
                self.assertEqual(cursor.fetchone()[0], 1)
                cursor.execute(
                    "SELECT id FROM corridas WHERE id_usuario = %s",
                    (user_id,),
                )
                ride_id = cursor.fetchone()[0]
        finally:
            connection.close()

        response = driver_client.post(
            f"/motorista/corridas/{ride_id}/iniciar"
        )
        self.assertEqual(response.status_code, 302)
        response = driver_client.post(
            f"/motorista/corridas/{ride_id}/finalizar",
            data={"distancia_km": "1.00"},
        )
        self.assertEqual(response.status_code, 302)

        response = driver_client.post(
            "/motorista/disponibilidade",
            data={"disponivel": "sim"},
        )
        self.assertEqual(response.status_code, 302)

        connection = self.database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT status, id_motorista FROM corridas WHERE id = %s",
                    (ride_id,),
                )
                self.assertEqual(cursor.fetchone(), ("Solicitada", None))
                cursor.execute(
                    "SELECT disponivel FROM motoristas WHERE id = %s",
                    (driver_id,),
                )
                self.assertFalse(cursor.fetchone()[0])
        finally:
            connection.close()

        response = driver_client.post(
            "/motorista/disponibilidade",
            data={"disponivel": "1"},
        )
        self.assertEqual(response.status_code, 302)

        response = driver_client.post(
            f"/motorista/corridas/{ride_id}/aceitar"
        )
        self.assertEqual(response.status_code, 302)
        response = driver_client.post(
            f"/motorista/corridas/{ride_id}/aceitar"
        )
        self.assertEqual(response.status_code, 302)
        response = user_client.post(
            f"/usuario/corridas/{ride_id}/cancelar"
        )
        self.assertEqual(response.status_code, 302)

        response = admin_client.post(
            f"/admin/motoristas/{driver_id}/status",
            data={"status": "Inativo"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"N\xc3\xa3o \xc3\xa9 poss\xc3\xadvel desativar", response.data)

        response = driver_client.post(
            f"/motorista/corridas/{ride_id}/finalizar",
            data={"distancia_km": "1.00"},
        )
        self.assertEqual(response.status_code, 302)

        response = driver_client.post(
            f"/motorista/corridas/{ride_id}/iniciar"
        )
        self.assertEqual(response.status_code, 302)

        response = driver_client.post(
            f"/motorista/corridas/{ride_id}/iniciar"
        )
        self.assertEqual(response.status_code, 302)

        for invalid_distance in ("abc", "0", "-1", "1.234", "NaN", "1000000"):
            with self.subTest(invalid_distance=invalid_distance):
                response = driver_client.post(
                    f"/motorista/corridas/{ride_id}/finalizar",
                    data={"distancia_km": invalid_distance},
                )
                self.assertEqual(response.status_code, 302)

        connection = self.database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT status, distancia_km, valor
                    FROM corridas
                    WHERE id = %s
                    """,
                    (ride_id,),
                )
                self.assertEqual(
                    cursor.fetchone(),
                    ("Em andamento", None, None),
                )
        finally:
            connection.close()

        response = driver_client.post(
            f"/motorista/corridas/{ride_id}/finalizar",
            data={"distancia_km": "4,20"},
        )
        self.assertEqual(response.status_code, 302)

        for payment_data in (
            {"corrida_id": str(ride_id), "forma_pagamento": "Criptomoeda"},
            {"corrida_id": "inválida", "forma_pagamento": "Pix"},
        ):
            with self.subTest(invalid_payment=payment_data):
                response = user_client.post(
                    "/usuario/pagamentos",
                    data=payment_data,
                )
                self.assertEqual(response.status_code, 302)

        response = user_client.post(
            "/usuario/pagamentos",
            data={"corrida_id": str(ride_id), "forma_pagamento": "Pix"},
        )
        self.assertEqual(response.status_code, 302)

        response = user_client.post(
            "/usuario/pagamentos",
            data={"corrida_id": str(ride_id), "forma_pagamento": "Pix"},
        )
        self.assertEqual(response.status_code, 302)

        for invalid_rating in ("0", "6", "texto"):
            with self.subTest(invalid_rating=invalid_rating):
                response = user_client.post(
                    f"/usuario/corridas/{ride_id}/avaliar",
                    data={"nota": invalid_rating, "comentario": ""},
                )
                self.assertEqual(response.status_code, 302)

        response = user_client.post(
            f"/usuario/corridas/{ride_id}/avaliar",
            data={"nota": "5", "comentario": "Viagem concluída com sucesso."},
        )
        self.assertEqual(response.status_code, 302)

        response = user_client.post(
            f"/usuario/corridas/{ride_id}/avaliar",
            data={"nota": "4", "comentario": "Avaliação duplicada."},
        )
        self.assertEqual(response.status_code, 302)

        connection = self.database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT status, id_motorista, distancia_km, valor
                    FROM corridas
                    WHERE id = %s
                    """,
                    (ride_id,),
                )
                ride = cursor.fetchone()
                self.assertEqual(
                    ride,
                    ("Finalizada", driver_id, Decimal("4.20"), Decimal("10.50")),
                )

                cursor.execute(
                    """
                    SELECT forma_pagamento, status, valor
                    FROM pagamentos
                    WHERE id_corrida = %s
                    """,
                    (ride_id,),
                )
                self.assertEqual(
                    cursor.fetchone(),
                    ("Pix", "Pendente", Decimal("10.50")),
                )

                cursor.execute(
                    "SELECT nota, comentario FROM avaliacoes WHERE id_corrida = %s",
                    (ride_id,),
                )
                self.assertEqual(
                    cursor.fetchone(),
                    (5, "Viagem concluída com sucesso."),
                )

                cursor.execute(
                    """
                    SELECT status_anterior, novo_status
                    FROM historico_corridas
                    WHERE id_corrida = %s
                    ORDER BY id
                    """,
                    (ride_id,),
                )
                self.assertEqual(
                    cursor.fetchall(),
                    [
                        ("Solicitada", "Aceita"),
                        ("Aceita", "Em andamento"),
                        ("Em andamento", "Finalizada"),
                    ],
                )
        finally:
            connection.close()

        for client, paths in (
            (
                user_client,
                (
                    "/usuario/home",
                    "/usuario/corridas",
                    "/usuario/pagamentos",
                    "/usuario/conta",
                ),
            ),
            (
                driver_client,
                (
                    "/motorista/home",
                    "/motorista/corridas-disponiveis",
                    "/motorista/historico",
                    "/motorista/conta",
                ),
            ),
            (
                admin_client,
                (
                    "/admin/home",
                    "/admin/usuarios",
                    "/admin/motoristas",
                    "/admin/corridas",
                    "/admin/pagamentos",
                    "/admin/avaliacoes",
                    "/admin/conta",
                ),
            ),
        ):
            for path in paths:
                with self.subTest(path=path):
                    self.assertEqual(client.get(path).status_code, 200)

        self.assertEqual(user_client.get("/admin/corridas").status_code, 403)
        self.assertEqual(driver_client.get("/admin/motoristas").status_code, 403)
        self.assertEqual(admin_client.get("/usuario/home").status_code, 403)


if __name__ == "__main__":
    unittest.main()

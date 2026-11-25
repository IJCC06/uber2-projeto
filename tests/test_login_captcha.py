import json
import unittest
from urllib.error import URLError
from urllib.parse import parse_qs
from unittest.mock import patch

import app as app_module
import blueprints.auth as auth_module


class FakeGoogleResponse:
    def __init__(self, result):
        self.content = json.dumps(result).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self, limit):
        return self.content[:limit]


class LoginCaptchaTests(unittest.TestCase):
    login_cases = (
        (
            "/login/usuario",
            {"email": "user@example.test", "password": "password"},
            "realizar_login_usuario",
        ),
        (
            "/login/motorista",
            {"cpf": "12345678900", "password": "password"},
            "realizar_login_motorista",
        ),
        (
            "/login/admin",
            {"email": "admin@example.test", "password": "password"},
            "realizar_login_admin",
        ),
    )

    def setUp(self):
        self.app = app_module.uber2
        self.original_recaptcha_config = (
            self.app.config.get("RECAPTCHA_SITE_KEY"),
            self.app.config.get("RECAPTCHA_SECRET_KEY"),
        )
        self.app.config.update(
            RECAPTCHA_SITE_KEY="test-site-key",
            RECAPTCHA_SECRET_KEY="test-secret-key",
        )
        self.client = self.app.test_client()

    def tearDown(self):
        (
            self.app.config["RECAPTCHA_SITE_KEY"],
            self.app.config["RECAPTCHA_SECRET_KEY"],
        ) = self.original_recaptcha_config

    def test_token_ausente_impede_todos_os_logins_sem_consultar_o_google(self):
        for path, data, login_function in self.login_cases:
            with self.subTest(path=path):
                with (
                    patch.object(auth_module, "urlopen") as consultar_google,
                    patch.object(auth_module, login_function) as validar_credenciais,
                ):
                    resposta = self.client.post(path, data=data)

                self.assertEqual(resposta.status_code, 200)
                self.assertIn(b"validar o CAPTCHA", resposta.data)
                consultar_google.assert_not_called()
                validar_credenciais.assert_not_called()

    def test_token_rejeitado_impede_todos_os_logins(self):
        for path, data, login_function in self.login_cases:
            with self.subTest(path=path):
                with (
                    patch.object(
                        auth_module,
                        "urlopen",
                        return_value=FakeGoogleResponse({"success": False}),
                    ),
                    patch.object(auth_module, login_function) as validar_credenciais,
                ):
                    dados = {**data, "g-recaptcha-response": "token-rejeitado"}
                    resposta = self.client.post(path, data=dados)

                self.assertEqual(resposta.status_code, 200)
                self.assertIn(b"validar o CAPTCHA", resposta.data)
                validar_credenciais.assert_not_called()

    def test_token_aceito_e_enviado_ao_validador_de_credenciais(self):
        for path, data, login_function in self.login_cases:
            with self.subTest(path=path):
                with (
                    patch.object(
                        auth_module,
                        "urlopen",
                        return_value=FakeGoogleResponse({"success": True}),
                    ) as consultar_google,
                    patch.object(
                        auth_module,
                        login_function,
                        return_value=None,
                    ) as validar_credenciais,
                ):
                    dados = {**data, "g-recaptcha-response": "token-aceito"}
                    resposta = self.client.post(path, data=dados)

                self.assertEqual(resposta.status_code, 200)
                self.assertNotIn(b"validar o CAPTCHA", resposta.data)
                validar_credenciais.assert_called_once()
                payload = parse_qs(
                    consultar_google.call_args.args[0].data.decode("ascii")
                )
                self.assertEqual(payload["secret"], ["test-secret-key"])
                self.assertEqual(payload["response"], ["token-aceito"])
                self.assertEqual(consultar_google.call_args.kwargs["timeout"], 5)

    def test_falha_de_rede_rejeita_o_login(self):
        with (
            patch.object(
                auth_module,
                "urlopen",
                side_effect=URLError("serviço indisponível"),
            ),
            patch.object(auth_module, "realizar_login_usuario") as validar_credenciais,
        ):
            resposta = self.client.post(
                "/login/usuario",
                data={
                    "email": "user@example.test",
                    "password": "password",
                    "g-recaptcha-response": "token",
                },
            )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"validar o CAPTCHA", resposta.data)
        validar_credenciais.assert_not_called()

    def test_chaves_ausentes_impedem_a_validacao_e_o_login(self):
        self.app.config["RECAPTCHA_SECRET_KEY"] = None

        with (
            patch.object(auth_module, "urlopen") as consultar_google,
            patch.object(
                auth_module,
                "realizar_login_usuario",
            ) as validar_credenciais,
        ):
            resposta = self.client.post(
                "/login/usuario",
                data={
                    "email": "user@example.test",
                    "password": "password",
                    "g-recaptcha-response": "token",
                },
            )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"validar o CAPTCHA", resposta.data)
        consultar_google.assert_not_called()
        validar_credenciais.assert_not_called()


if __name__ == "__main__":
    unittest.main()

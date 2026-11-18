import unittest

import app as app_module


class LoginTemplateTests(unittest.TestCase):
    def setUp(self):
        self.client = app_module.uber2.test_client()

    def test_usuario_e_motorista_veem_telas_de_login_com_bootstrap(self):
        resposta = self.client.get("/")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"vendor/bootstrap/bootstrap.min.css", resposta.data)
        self.assertIn(b'class="row g-3"', resposta.data)
        self.assertIn(b'class="form-control"', resposta.data)
        self.assertIn(b'action="/login/usuario"', resposta.data)
        self.assertIn(b'action="/login/motorista"', resposta.data)
        self.assertIn(b'id="email"', resposta.data)
        self.assertIn(b'id="user-password"', resposta.data)
        self.assertIn(b'id="cpf"', resposta.data)
        self.assertIn(b'id="driver-password"', resposta.data)

    def test_administrador_ve_tela_de_login_com_bootstrap(self):
        resposta = self.client.get("/login/admin")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"vendor/bootstrap/bootstrap.min.css", resposta.data)
        self.assertIn(b'class="vstack gap-3"', resposta.data)
        self.assertIn(b'class="form-control"', resposta.data)
        self.assertIn(b'action="/login/admin"', resposta.data)
        self.assertIn(b'id="admin-email"', resposta.data)
        self.assertIn(b'id="admin-password"', resposta.data)

    def test_arquivo_local_do_bootstrap_e_servido(self):
        resposta = self.client.get("/static/vendor/bootstrap/bootstrap.min.css")

        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.mimetype.startswith("text/css"))
        self.assertIn(b".form-control", resposta.data)
        resposta.close()

    def test_css_personalizado_dos_cadastros_preserva_layout_dos_formularios(self):
        resposta = self.client.get("/static/css/login.css")
        css = resposta.get_data(as_text=True).replace("\r\n", "\n")
        resposta.close()

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(".login-form {\n    display: grid;\n    gap: 18px;", css)
        self.assertIn(".form-field {\n    display: grid;\n    gap: 8px;", css)


if __name__ == "__main__":
    unittest.main()

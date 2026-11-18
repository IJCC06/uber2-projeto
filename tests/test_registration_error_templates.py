import unittest
from pathlib import Path

from flask import render_template

import app as app_module


class RegistrationErrorTemplateTests(unittest.TestCase):
    def test_cadastros_usam_bootstrap_e_mantem_campos(self):
        templates = [
            ("logins/cadastro.html", "cadastro"),
            ("logins/cadastro_motorista.html", "cadastro_motorista"),
        ]
        with app_module.uber2.test_request_context("/"):
            for template_name, kind in templates:
                with self.subTest(template=template_name):
                    html = render_template(template_name)
                    self.assertIn("vendor/bootstrap/bootstrap.min.css", html)
                    self.assertIn('class="form-control"', html)
                    self.assertIn('type="password"', html)
                    if kind == "cadastro":
                        self.assertIn('name="email"', html)
                        self.assertIn('action="/cadastro"', html)
                    else:
                        self.assertIn('name="cpf"', html)
                        self.assertIn('name="cnh"', html)
                        self.assertIn('action="/cadastro/motorista"', html)

    def test_pagina_de_erro_usa_bootstrap_sem_css_legado(self):
        with app_module.uber2.test_request_context("/"):
            html = render_template(
                "errors/error.html",
                status_code=404,
                titulo="Página não encontrada",
                mensagem="O endereço solicitado não existe.",
            )

        self.assertIn("vendor/bootstrap/bootstrap.min.css", html)
        self.assertIn("Erro 404", html)
        self.assertIn("Página não encontrada", html)
        self.assertIn("Voltar ao início", html)
        self.assertNotIn("css/errors.css", html)

    def test_cadastros_e_erros_referenciam_bootstrap(self):
        templates_root = Path(__file__).resolve().parents[1] / "templates"
        public_templates = [
            templates_root / "logins" / "cadastro.html",
            templates_root / "logins" / "cadastro_motorista.html",
            templates_root / "errors" / "error.html",
        ]
        for template in public_templates:
            with self.subTest(template=template.name):
                conteudo = template.read_text(encoding="utf-8")
                self.assertIn("vendor/bootstrap/bootstrap.min.css", conteudo)


if __name__ == "__main__":
    unittest.main()

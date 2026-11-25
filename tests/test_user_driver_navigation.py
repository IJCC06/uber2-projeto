import unittest
from pathlib import Path

from flask import render_template

import app as app_module


class UserDriverNavigationTests(unittest.TestCase):
    def test_navegacao_de_usuario_usa_componentes_bootstrap(self):
        with app_module.uber2.test_request_context("/"):
            html = render_template("includes/header_usuario.html")

        self.assertIn('class="nav nav-pills flex-wrap"', html)
        self.assertIn("Solicitar corrida", html)
        self.assertIn("Minhas corridas", html)
        self.assertIn("Pagamentos", html)
        self.assertIn('method="POST"', html)
        self.assertIn('class="btn btn-outline-dark btn-sm"', html)

    def test_navegacao_de_motorista_usa_componentes_bootstrap(self):
        with app_module.uber2.test_request_context("/"):
            html = render_template("includes/header_motorista.html")

        self.assertIn('class="nav nav-pills flex-wrap"', html)
        self.assertIn("Corridas disponíveis", html)
        self.assertIn("Histórico", html)
        self.assertIn("Meus veículos", html)
        self.assertIn('method="POST"', html)
        self.assertIn('class="btn btn-outline-dark btn-sm"', html)

    def test_telas_de_usuario_e_motorista_carregam_bootstrap_local(self):
        templates_root = Path(__file__).resolve().parents[1] / "templates"
        templates = list((templates_root / "usuarios").glob("*.html"))
        templates.extend((templates_root / "motoristas").glob("*.html"))

        self.assertTrue(templates)
        for template in templates:
            with self.subTest(template=template.relative_to(templates_root)):
                conteudo = template.read_text(encoding="utf-8")
                self.assertIn("vendor/bootstrap/bootstrap.min.css", conteudo)


if __name__ == "__main__":
    unittest.main()

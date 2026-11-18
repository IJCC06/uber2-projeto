import unittest
from pathlib import Path

from flask import render_template

import app as app_module


class AdminNavigationTests(unittest.TestCase):
    def test_navegacao_administrativa_usa_componentes_bootstrap(self):
        with app_module.uber2.test_request_context("/"):
            html = render_template("includes/header_admin.html")

        self.assertIn('class="nav nav-pills flex-wrap"', html)
        self.assertIn('class="nav-link', html)
        self.assertIn("Painel administrativo", html)
        self.assertIn("Usuários", html)
        self.assertIn("Motoristas", html)
        self.assertIn("Avaliações", html)
        self.assertIn('method="POST"', html)
        self.assertIn('class="btn btn-outline-dark btn-sm"', html)

    def test_todas_as_telas_administrativas_carregam_bootstrap_local(self):
        templates_dir = Path(__file__).resolve().parents[1] / "templates" / "admins"
        templates = list(templates_dir.glob("*.html"))

        self.assertTrue(templates)
        for template in templates:
            with self.subTest(template=template.name):
                conteudo = template.read_text(encoding="utf-8")
                self.assertIn("vendor/bootstrap/bootstrap.min.css", conteudo)


if __name__ == "__main__":
    unittest.main()

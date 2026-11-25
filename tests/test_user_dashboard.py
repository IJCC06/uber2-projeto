import unittest
from datetime import datetime
from types import SimpleNamespace

from flask import render_template

import app as app_module


class UserDashboardTests(unittest.TestCase):
    def render_dashboard(self, corridas_recentes):
        with app_module.uber2.test_request_context("/"):
            return render_template(
                "usuarios/home_usuarios.html",
                current_user=SimpleNamespace(nome="Ana"),
                corridas_realizadas=4,
                corridas_ativas=1,
                pagamentos_pendentes=2,
                corridas_recentes=corridas_recentes,
            )

    def test_painel_mostra_resumo_e_dados_da_corrida_com_bootstrap(self):
        corrida = SimpleNamespace(
            id=42,
            origem="Centro",
            destino="Aeroporto",
            status="Finalizada",
            data_hora=datetime(2026, 1, 15, 9, 30),
            motorista="João",
            valor=25.5,
        )

        html = self.render_dashboard([corrida])

        self.assertIn('class="container-xl py-5"', html)
        self.assertIn('class="row g-3 mb-4"', html)
        self.assertIn("Olá, Ana!", html)
        self.assertIn("Corridas realizadas", html)
        self.assertIn(">4</strong>", html)
        self.assertIn("Corrida #42", html)
        self.assertIn("Centro", html)
        self.assertIn("Aeroporto", html)
        self.assertIn('class="badge rounded-pill text-bg-success"', html)
        self.assertIn("15/01/2026 às 09:30", html)
        self.assertIn("R$ 25,50", html)

    def test_painel_mostra_estado_vazio_e_acao_para_primeira_corrida(self):
        html = self.render_dashboard([])

        self.assertIn("Nenhuma corrida encontrada", html)
        self.assertIn("Quando você solicitar uma corrida, ela aparecerá aqui.", html)
        self.assertIn("Solicitar a primeira corrida", html)


if __name__ == "__main__":
    unittest.main()

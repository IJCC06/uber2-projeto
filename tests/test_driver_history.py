import unittest
from datetime import datetime
from types import SimpleNamespace

from flask import render_template

import app as app_module


class DriverHistoryTests(unittest.TestCase):
    def render_history(self, corridas):
        with app_module.uber2.test_request_context("/"):
            return render_template(
                "motoristas/historico_corridas.html",
                corridas=corridas,
                corridas_finalizadas=1,
                total_recebido=21.25,
            )

    def test_historico_mostra_valores_status_e_distancia_com_bootstrap(self):
        data_hora = datetime(2026, 3, 5, 11, 45)
        corrida_finalizada = SimpleNamespace(
            id=24,
            usuario="Ana",
            origem="Centro",
            destino="Aeroporto",
            data_hora=data_hora,
            status="Finalizada",
            distancia_km=8.5,
            valor=21.25,
        )
        corrida_cancelada = SimpleNamespace(
            id=23,
            usuario="Bruno",
            origem="Estação",
            destino="Hospital",
            data_hora=data_hora,
            status="Cancelada",
            distancia_km=None,
            valor=None,
        )

        html = self.render_history([corrida_finalizada, corrida_cancelada])

        self.assertIn('class="container-xl py-5"', html)
        self.assertIn("Corridas finalizadas", html)
        self.assertIn("R$ 21,25", html)
        self.assertIn("Corrida #24", html)
        self.assertIn("Corrida #23", html)
        self.assertIn('class="badge rounded-pill text-bg-success"', html)
        self.assertIn('class="badge rounded-pill text-bg-danger"', html)
        self.assertIn("8,50 km", html)
        self.assertIn("Não definido", html)
        self.assertEqual(html.count("Distância"), 1)
        self.assertIn("Baixar histórico PDF", html)

    def test_historico_vazio_mantem_atalho_para_corridas_disponiveis(self):
        html = self.render_history([])

        self.assertIn("Nenhuma corrida anterior", html)
        self.assertIn("As corridas finalizadas ou canceladas aparecerão aqui.", html)
        self.assertIn("Consultar corridas disponíveis", html)


if __name__ == "__main__":
    unittest.main()

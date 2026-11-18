import unittest
from datetime import datetime
from types import SimpleNamespace

from flask import render_template

import app as app_module


class DriverDashboardTests(unittest.TestCase):
    def render_dashboard(self, **context):
        context.setdefault("current_user", SimpleNamespace(nome="Carlos"))
        with app_module.uber2.test_request_context("/"):
            return render_template("motoristas/home_motorista.html", **context)

    def test_painel_inicial_mostra_proximo_passo_com_bootstrap(self):
        html = self.render_dashboard()

        self.assertIn('class="container-xl py-5"', html)
        self.assertIn("Olá, Carlos!", html)
        self.assertIn("Próximo passo", html)
        self.assertIn("Consultar corridas", html)

    def test_painel_renderiza_corridas_avaliacoes_e_acoes(self):
        data_hora = datetime(2026, 2, 10, 14, 30)
        corrida_aceita = SimpleNamespace(
            id=12,
            status="Aceita",
            usuario="Ana",
            origem="Centro",
            destino="Aeroporto",
            data_hora=data_hora,
        )
        corrida_em_andamento = SimpleNamespace(
            id=13,
            status="Em andamento",
            usuario="Bruno",
            origem="Estação",
            destino="Hospital",
            data_hora=data_hora,
        )
        avaliacao = SimpleNamespace(
            nota=5,
            data=data_hora,
            usuario="Ana",
            corrida_id=12,
            comentario=None,
        )
        corrida_disponivel = SimpleNamespace(
            id=14,
            data_hora=data_hora,
            usuario="Beatriz",
            origem="Centro",
            destino="Aeroporto",
        )

        html = self.render_dashboard(
            pode_receber=True,
            motorista_ativo=True,
            disponivel=True,
            avaliacoes_recentes=[avaliacao],
            quantidade_avaliacoes=1,
            media_avaliacoes=5.0,
            corridas_ativas=[corrida_aceita, corrida_em_andamento],
            corridas_disponiveis=[corrida_disponivel],
        )

        self.assertIn("Você está disponível", html)
        self.assertIn('name="disponivel" value="0"', html)
        self.assertIn("Ficar indisponível", html)
        self.assertIn("Baixar avaliações PDF", html)
        self.assertIn("5,00", html)
        self.assertIn("O passageiro não deixou um comentário.", html)
        self.assertIn("Iniciar corrida", html)
        self.assertIn("Cancelar corrida", html)
        self.assertIn("return confirm('Deseja cancelar esta corrida?');", html)
        self.assertIn('name="distancia_km"', html)
        self.assertIn("Finalizar corrida", html)
        self.assertIn("Aceitar corrida", html)

    def test_painel_exibe_estados_vazios_e_conta_inativa(self):
        html = self.render_dashboard(
            pode_receber=False,
            motorista_ativo=False,
            disponivel=False,
            avaliacoes_recentes=[],
            quantidade_avaliacoes=0,
            media_avaliacoes=None,
            corridas_ativas=[],
            corridas_disponiveis=[],
        )

        self.assertIn("Sua conta está inativa", html)
        self.assertIn("Disponibilidade desativada", html)
        self.assertIn("Você ainda não recebeu avaliações", html)
        self.assertIn("Nenhuma corrida atribuída", html)
        self.assertNotIn("Ficar disponível", html)


if __name__ == "__main__":
    unittest.main()

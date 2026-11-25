import unittest
from datetime import datetime
from types import SimpleNamespace

from flask import render_template

import app as app_module


class UserProfilePageTests(unittest.TestCase):
    def test_solicitacao_mantem_campos_e_destino(self):
        with app_module.uber2.test_request_context("/"):
            html = render_template("usuarios/solicitar_corrida.html", erro=None)

        self.assertIn("vendor/bootstrap/bootstrap.min.css", html)
        self.assertIn('name="origem"', html)
        self.assertIn('name="destino"', html)
        self.assertIn("Solicitar corrida", html)
        self.assertIn('action="/usuario/corridas/solicitar"', html)

    def test_minhas_corridas_preserva_acoes_cancelamento_avaliacao_e_pdf(self):
        corrida = SimpleNamespace(
            id=31,
            origem="Centro",
            destino="Aeroporto",
            status="Finalizada",
            data_hora=datetime(2026, 4, 3, 10, 15),
            motorista="João",
            distancia_km=12.5,
            valor=31.25,
            nota=None,
            comentario=None,
        )

        with app_module.uber2.test_request_context("/"):
            html = render_template("usuarios/minhas_corridas.html", corridas=[corrida])

        self.assertIn("vendor/bootstrap/bootstrap.min.css", html)
        self.assertIn("Corrida #31", html)
        self.assertIn("Centro", html)
        self.assertIn("Aeroporto", html)
        self.assertIn("12,50 km", html)
        self.assertIn("R$ 31,25", html)
        self.assertIn("Enviar avaliação", html)
        self.assertIn('name="nota"', html)
        self.assertIn('name="comentario"', html)
        self.assertIn("Baixar histórico PDF", html)
        self.assertIn("Ver pagamento", html)

    def test_pagamentos_preserva_registro_formas_e_estado_vazio(self):
        corrida = SimpleNamespace(
            id=32,
            origem="Estação",
            destino="Hospital",
            distancia_km=7.2,
            valor=18.0,
            forma_pagamento=None,
            status_pagamento=None,
        )

        with app_module.uber2.test_request_context("/"):
            html = render_template("usuarios/pagamentos.html", corridas=[corrida])
            empty_html = render_template("usuarios/pagamentos.html", corridas=[])

        self.assertIn("Registrar pagamento", html)
        self.assertIn('name="corrida_id" value="32"', html)
        self.assertIn('name="forma_pagamento"', html)
        self.assertIn("Pix", html)
        self.assertIn("Dinheiro", html)
        self.assertIn("Cartão", html)
        self.assertIn("Nenhuma corrida finalizada", empty_html)
        self.assertIn("Baixar extrato PDF", html)

    def test_conta_preserva_dados_e_alteracao_opcional_de_senha(self):
        usuario = SimpleNamespace(
            nome="Ana Souza",
            email="ana@example.com",
            telefone="11988887777",
        )

        with app_module.uber2.test_request_context("/"):
            html = render_template("usuarios/conta.html", usuario=usuario)

        self.assertIn("vendor/bootstrap/bootstrap.min.css", html)
        self.assertIn('value="Ana Souza"', html)
        self.assertIn('value="ana@example.com"', html)
        self.assertIn('name="telefone"', html)
        self.assertIn("Alterar senha (opcional)", html)
        self.assertIn('name="senha_atual"', html)
        self.assertIn('name="nova_senha"', html)
        self.assertIn('name="confirmar_senha"', html)
        password_fields = html.split("<fieldset", 1)[1].split("</fieldset>", 1)[0]
        self.assertNotIn("required", password_fields)


if __name__ == "__main__":
    unittest.main()

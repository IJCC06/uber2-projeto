import unittest
from datetime import datetime
from types import SimpleNamespace

from flask import render_template

import app as app_module


class AdminPageTests(unittest.TestCase):
    def test_usuarios_mantem_busca_status_pdf_e_conta(self):
        usuario = SimpleNamespace(
            id=3,
            nome="Ana",
            email="ana@example.com",
            telefone="11999999999",
            data_cadastro=datetime(2026, 1, 10),
            ativo=True,
        )
        with app_module.uber2.test_request_context("/"):
            html = render_template(
                "admins/usuarios.html",
                usuarios=[usuario],
                busca="Ana",
            )

        self.assertIn('class="container-xl py-5"', html)
        self.assertIn("Ana", html)
        self.assertIn('name="busca" type="search"', html)
        self.assertIn('name="ativo" value="0"', html)
        self.assertIn("Desativar conta", html)
        self.assertIn("Exportar PDF", html)

    def test_motoristas_mantem_busca_disponibilidade_status_e_pdf(self):
        motorista = SimpleNamespace(
            id=4,
            nome="Carlos",
            cpf="12345678900",
            telefone="11888888888",
            cnh="123456",
            disponivel=True,
            ativo=True,
        )
        with app_module.uber2.test_request_context("/"):
            html = render_template(
                "admins/motoristas.html",
                motoristas=[motorista],
                busca="Carlos",
            )

        self.assertIn("Carlos", html)
        self.assertIn("Disponível", html)
        self.assertIn('name="status"', html)
        self.assertIn("Desativar conta", html)
        self.assertIn("Exportar PDF", html)

    def test_corridas_mantem_filtro_pdf_pagamento_avaliacao_e_timeline(self):
        corrida = SimpleNamespace(
            id=8,
            origem="Centro",
            destino="Aeroporto",
            status="Finalizada",
            usuario="Ana",
            motorista="Carlos",
            data_hora=datetime(2026, 2, 2, 10, 30),
            distancia_km=10.5,
            valor=26.25,
            pagamento=SimpleNamespace(forma="Pix", status="Pendente", valor=26.25),
            avaliacao=SimpleNamespace(nota=5, comentario="Excelente"),
            historico=[],
        )
        with app_module.uber2.test_request_context("/"):
            html = render_template(
                "admins/corridas.html",
                corridas=[corrida],
                status_filtro="Finalizada",
                status_validos=["Solicitada", "Finalizada"],
            )

        self.assertIn('name="status"', html)
        self.assertIn("Centro", html)
        self.assertIn("Pix", html)
        self.assertIn("5/5", html)
        self.assertIn("Exportar PDF", html)

    def test_pagamentos_avaliacoes_e_conta_renderizam_componentes_bootstrap(self):
        with app_module.uber2.test_request_context("/"):
            pagamentos = render_template(
                "admins/pagamentos.html",
                total_pendentes=1,
                valor_pendente=20,
                total_pagos=0,
                valor_pago=0,
                total_pagamentos=1,
                pagamentos=[],
                status_filtro=None,
                forma_filtro=None,
                status_validos=["Pendente", "Pago"],
                formas_validas=["Pix", "Dinheiro", "Cartão"],
            )
            avaliacoes = render_template(
                "admins/avaliacoes.html",
                total_avaliacoes=0,
                media_avaliacoes=None,
                avaliacoes=[],
                nota_filtro=None,
                notas_validas=[1, 2, 3, 4, 5],
            )
            conta = render_template(
                "admins/conta.html",
                administrador=SimpleNamespace(
                    nome="Administrador",
                    email="admin@example.com",
                ),
            )

        self.assertIn('class="row g-3 mb-4"', pagamentos)
        self.assertIn("Nenhum pagamento encontrado", pagamentos)
        self.assertIn("Exportar PDF", pagamentos)
        self.assertIn('name="forma"', pagamentos)
        self.assertIn("Nenhuma avaliação encontrada", avaliacoes)
        self.assertIn('name="nota"', avaliacoes)
        self.assertIn('value="Administrador"', conta)
        self.assertIn('name="senha_atual"', conta)
        self.assertIn("Alterar senha (opcional)", conta)


if __name__ == "__main__":
    unittest.main()

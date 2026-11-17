import re
import unittest

from flask import Flask

from python.pdf_export import enviar_relatorio_pdf


class EnviarRelatorioPDFTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_gera_anexo_pdf_com_dados_em_portugues(self):
        registros = [
            (
                "Corrida #1",
                (
                    ("Passageiro", "João da Silva"),
                    ("Comentário", "Ótimo trajeto em São Paulo 🚗"),
                ),
            )
        ]
        with self.app.test_request_context("/"):
            resposta = enviar_relatorio_pdf(
                "Relatório de corridas",
                registros,
                "corridas.pdf",
            )
            resposta.direct_passthrough = False
            conteudo = resposta.get_data()

        self.assertTrue(conteudo.startswith(b"%PDF-"))
        self.assertEqual(resposta.mimetype, "application/pdf")
        self.assertIn(
            "attachment; filename=corridas.pdf",
            resposta.headers["Content-Disposition"],
        )
        self.assertEqual(resposta.headers["Cache-Control"], "private, no-store")

    def test_relatorios_longos_criam_paginas_adicionais(self):
        registros = [
            (f"Corrida #{indice}", (("Origem", "Rua de teste"),))
            for indice in range(100)
        ]
        with self.app.test_request_context("/"):
            resposta = enviar_relatorio_pdf(
                "Histórico de corridas",
                registros,
                "historico.pdf",
            )
            resposta.direct_passthrough = False
            conteudo = resposta.get_data()

        self.assertGreaterEqual(len(re.findall(rb"/Type /Page\b", conteudo)), 2)

    def test_relatorio_sem_registros_continua_sendo_um_pdf_valido(self):
        with self.app.test_request_context("/"):
            resposta = enviar_relatorio_pdf(
                "Relatório vazio",
                [],
                "relatorio-vazio.pdf",
            )
            resposta.direct_passthrough = False
            conteudo = resposta.get_data()

        self.assertTrue(conteudo.startswith(b"%PDF-"))


if __name__ == "__main__":
    unittest.main()

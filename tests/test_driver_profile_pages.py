import unittest
from types import SimpleNamespace

from flask import render_template, url_for

import app as app_module


class DriverProfilePageTests(unittest.TestCase):
    def test_vehicle_page_preserves_create_edit_delete_and_pdf_actions(self):
        veiculos = [
            {
                "id": 7,
                "marca": "Honda",
                "modelo": "Civic",
                "placa": "ABC1D23",
                "ano": 2022,
                "cor": "Azul",
            },
            {
                "id": 8,
                "marca": "Fiat",
                "modelo": "Argo",
                "placa": "DEF4G56",
                "ano": 2021,
                "cor": None,
            },
        ]

        with app_module.uber2.test_request_context("/"):
            html = render_template("motoristas/meus_veiculos.html", veiculos=veiculos)
            edit_action = url_for("motoristas.editar_veiculo", veiculo_id=7)
            delete_action = url_for("motoristas.excluir_veiculo", veiculo_id=7)
            export_url = url_for("motoristas.exportar_veiculos_pdf")

        self.assertIn("vendor/bootstrap/bootstrap.min.css", html)
        self.assertIn('name="marca" maxlength="50"', html)
        self.assertIn('name="ano" type="number" min="1" step="1" required', html)
        self.assertIn(f'action="{edit_action}"', html)
        self.assertIn(f'action="{delete_action}"', html)
        self.assertIn(f'href="{export_url}"', html)
        self.assertIn("Salvar alterações", html)
        self.assertIn("return confirm('Deseja excluir este veículo?');", html)
        self.assertIn("Honda", html)
        self.assertIn("Azul", html)
        self.assertEqual(html.count('<dt class="small text-body-secondary mb-1">Cor</dt>'), 1)

    def test_vehicle_page_shows_empty_state(self):
        with app_module.uber2.test_request_context("/"):
            html = render_template("motoristas/meus_veiculos.html", veiculos=[])

        self.assertIn("Nenhum veículo cadastrado", html)
        self.assertIn("Use o formulário acima para cadastrar seu primeiro veículo.", html)

    def test_account_page_preserves_profile_and_optional_password_fields(self):
        motorista = SimpleNamespace(
            nome="Carlos Silva",
            cpf="123.456.789-00",
            telefone="11999999999",
            cnh="CNH123456",
        )

        with app_module.uber2.test_request_context("/"):
            html = render_template("motoristas/conta.html", motorista=motorista)
            account_url = url_for("motoristas.conta")

        self.assertIn("vendor/bootstrap/bootstrap.min.css", html)
        self.assertIn(f'action="{account_url}" method="post"', html)
        self.assertIn('name="nome"', html)
        self.assertIn('value="Carlos Silva"', html)
        self.assertIn('name="cpf"', html)
        self.assertIn('name="telefone"', html)
        self.assertIn('name="cnh"', html)
        self.assertIn("Deixe os campos de senha vazios para manter sua senha atual.", html)
        self.assertIn('name="senha_atual"', html)
        self.assertIn('name="nova_senha"', html)
        self.assertIn('name="confirmar_senha"', html)
        self.assertIn('minlength="8"', html)
        password_fields = html.split("<fieldset", 1)[1].split("</fieldset>", 1)[0]
        self.assertNotIn("required", password_fields)


if __name__ == "__main__":
    unittest.main()

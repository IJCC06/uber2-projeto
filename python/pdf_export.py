from datetime import date, datetime
from io import BytesIO

from flask import abort, current_app, send_file
from fpdf import FPDF
import psycopg2

from conexao import criar_conexao


class _RelatorioPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.cell(0, 8, self._texto(f"Página {self.page_no()}"), align="C")

    @staticmethod
    def _texto(valor):
        return str(valor).encode("latin-1", errors="replace").decode("latin-1")


def formatar_data(valor):
    if isinstance(valor, (date, datetime)):
        return valor.strftime("%d/%m/%Y %H:%M")
    return "Não informado"


def formatar_moeda(valor):
    if valor is None:
        return "Não informado"
    return f"R$ {valor:.2f}".replace(".", ",")


def consultar_registros(consulta, parametros, mensagem_erro):
    conexao = None
    try:
        conexao = criar_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(consulta, parametros)
            return cursor.fetchall()
    except psycopg2.Error:
        if conexao is not None:
            conexao.rollback()
        current_app.logger.exception(mensagem_erro)
        abort(500)
    finally:
        if conexao is not None:
            conexao.close()


def enviar_relatorio_pdf(titulo, registros, nome_arquivo, resumo=()):
    pdf = _RelatorioPDF()
    pdf.set_title(pdf._texto(titulo))
    pdf.set_author("Uber 2")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    pdf.set_font("Helvetica", style="B", size=16)
    pdf.multi_cell(
        0,
        10,
        pdf._texto(titulo),
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.set_font("Helvetica", size=9)
    pdf.cell(
        0,
        7,
        pdf._texto(f"Gerado em {datetime.now().astimezone():%d/%m/%Y às %H:%M}"),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    for item in resumo:
        pdf.cell(0, 6, pdf._texto(item), new_x="LMARGIN", new_y="NEXT")
    if resumo:
        pdf.ln(3)

    if not registros:
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(
            0,
            7,
            pdf._texto("Nenhum registro encontrado."),
            new_x="LMARGIN",
            new_y="NEXT",
        )
    else:
        for titulo_registro, campos in registros:
            if pdf.get_y() > pdf.page_break_trigger - 20:
                pdf.add_page()
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.multi_cell(
                0,
                7,
                pdf._texto(titulo_registro),
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.set_font("Helvetica", size=9)
            for rotulo, valor in campos:
                pdf.multi_cell(
                    0,
                    5,
                    pdf._texto(f"{rotulo}: {valor}"),
                    new_x="LMARGIN",
                    new_y="NEXT",
                )
            pdf.ln(3)

    conteudo = BytesIO(bytes(pdf.output()))
    resposta = send_file(
        conteudo,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=nome_arquivo,
    )
    resposta.headers["Cache-Control"] = "private, no-store"
    return resposta

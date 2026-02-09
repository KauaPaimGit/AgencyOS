"""
ContractService v1.2.1
=======================
Gera minutas de contrato em PDF com design corporativo Vyron System.

Puxa automaticamente:
  • Nome do cliente
  • Valor do contrato
  • Datas do projeto (início / término)
  • Descrição / Tipo do projeto

Utiliza fpdf2 com layout profissional e cores Vivid Violet.

Autor: Vyron System Engine
"""

from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from sqlalchemy.orm import Session

from app import models


# ────────────────────────────────────────────────────────
# CONSTANTES DE DESIGN (Vivid Violet Theme)
# ────────────────────────────────────────────────────────
_VIOLET = (112, 0, 255)
_DEEP_INDIGO = (45, 55, 72)
_DARK_SLATE = (23, 25, 35)
_ICE_BLUE = (160, 174, 192)
_WHITE = (255, 255, 255)
_BLACK = (0, 0, 0)
_LIGHT_GRAY = (240, 240, 245)
_GRAY_TEXT = (100, 100, 100)
_SEPARATOR = (200, 200, 210)

_NL = {"new_x": XPos.LMARGIN, "new_y": YPos.NEXT}
_RT = {"new_x": XPos.RIGHT, "new_y": YPos.TOP}


# ────────────────────────────────────────────────────────
# HELPERS
# ────────────────────────────────────────────────────────
def _safe(value, fallback: str = "N/A") -> str:
    if value is None:
        return fallback
    return str(value).encode("latin-1", "replace").decode("latin-1")


def _format_brl(value) -> str:
    try:
        v = float(Decimal(str(value))) if value else 0.0
    except Exception:
        v = 0.0
    return f"R$ {v:,.2f}"


def _format_date(d) -> str:
    if isinstance(d, (date, datetime)):
        return d.strftime("%d/%m/%Y")
    return "A definir"


def _extenso_brl(valor: float) -> str:
    """Retorna valor por extenso simplificado."""
    inteiro = int(valor)
    centavos = int(round((valor - inteiro) * 100))
    # Simplificado — retorna formato numérico descritivo
    if centavos > 0:
        return f"{inteiro:,} reais e {centavos} centavos".replace(",", ".")
    return f"{inteiro:,} reais".replace(",", ".")


# ────────────────────────────────────────────────────────
# CLASSE PDF PARA CONTRATO
# ────────────────────────────────────────────────────────
class ContractPDF(FPDF):
    """PDF personalizado para minutas de contrato Vyron System."""

    def __init__(self, contract_number: str = ""):
        super().__init__()
        self._contract_number = contract_number

    def header(self):
        # Barra superior Vivid Violet
        self.set_fill_color(*_VIOLET)
        self.rect(0, 0, 210, 18, "F")

        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*_WHITE)
        self.set_y(3)
        self.cell(0, 8, "VYRON SYSTEM  |  Minuta de Contrato", border=0, align="C", **_NL)

        self.set_font("Helvetica", "", 8)
        self.set_text_color(220, 220, 240)
        self.cell(0, 5, f"Contrato {self._contract_number}", border=0, align="C", **_NL)
        self.ln(4)

    def footer(self):
        self.set_y(-16)
        self.set_draw_color(*_SEPARATOR)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())

        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*_GRAY_TEXT)
        ts = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(95, 10, f"Gerado em {ts} | Vyron System v1.2.1", border=0, align="L", **_RT)
        self.cell(95, 10, f"Pagina {self.page_no()}/{{nb}}", border=0, align="R", **_RT)

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*_VIOLET)
        self.cell(0, 9, title, border=0, align="L", **_NL)
        self.ln(1)

    def clause_header(self, number: str, title: str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*_DEEP_INDIGO)
        self.cell(0, 7, f"CLAUSULA {number} - {title}", border=0, align="L", **_NL)
        self.ln(1)

    def clause_body(self, text: str):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*_BLACK)
        self.multi_cell(0, 5, text, border=0, align="J", **_NL)
        self.ln(3)


# ────────────────────────────────────────────────────────
# SERVIÇO PRINCIPAL
# ────────────────────────────────────────────────────────
class ContractService:
    """
    Servico de geracao de minutas de contrato em PDF.

    Puxa dados do Project, Client e gera um documento estruturado
    com clausulas padrao de prestacao de servicos digitais.
    """

    @staticmethod
    def generate_contract_number(project_id: str) -> str:
        """Gera numero de contrato unico baseado no projeto."""
        now = datetime.now()
        short_id = str(project_id)[:8].upper()
        return f"VY-{now.year}{now.month:02d}-{short_id}"

    @staticmethod
    def generate(db: Session, project_id: str) -> tuple[bytes, str]:
        """
        Gera minuta de contrato em PDF para um projeto.

        Args:
            db: Sessao SQLAlchemy.
            project_id: UUID do projeto.

        Returns:
            Tupla (pdf_bytes, contract_number).

        Raises:
            ValueError: projeto nao encontrado.
        """
        # 1. Buscar dados
        project = (
            db.query(models.Project)
            .filter(models.Project.id == project_id)
            .first()
        )
        if not project:
            raise ValueError(f"Projeto {project_id} nao encontrado")

        client = project.client
        client_name = _safe(client.name) if client else "Cliente Nao Identificado"
        client_email = _safe(client.email if client else None, "N/A")
        client_company = _safe(
            getattr(client, "company_name", None) or (client.name if client else ""),
            "N/A"
        )

        project_name = _safe(project.name)
        contract_value = float(project.contract_value) if project.contract_value else 0.0
        start_date = project.start_date
        end_date = project.end_date

        contract_number = ContractService.generate_contract_number(project_id)

        # 2. Montar PDF
        pdf = ContractPDF(contract_number=contract_number)
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=20)

        # ── Titulo ──
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(*_DEEP_INDIGO)
        pdf.cell(0, 12, "CONTRATO DE PRESTACAO DE SERVICOS", border=0, align="C", **_NL)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*_GRAY_TEXT)
        pdf.cell(0, 7, "Servicos de Marketing Digital e Tecnologia", border=0, align="C", **_NL)
        pdf.ln(6)

        # ── Informacoes das Partes ──
        pdf.section_title("IDENTIFICACAO DAS PARTES")

        # Contratada
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*_DEEP_INDIGO)
        pdf.cell(0, 6, "CONTRATADA:", border=0, align="L", **_NL)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*_BLACK)
        pdf.multi_cell(0, 5,
            "Vyron System Tecnologia e Marketing Digital\n"
            "CNPJ: [A DEFINIR]\n"
            "Endereco: [A DEFINIR]",
            border=0, **_NL)
        pdf.ln(3)

        # Contratante
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*_DEEP_INDIGO)
        pdf.cell(0, 6, "CONTRATANTE:", border=0, align="L", **_NL)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*_BLACK)
        pdf.multi_cell(0, 5,
            f"Nome/Razao Social: {client_name}\n"
            f"Empresa: {client_company}\n"
            f"E-mail: {client_email}",
            border=0, **_NL)
        pdf.ln(4)

        # ── Separador ──
        pdf.set_draw_color(*_SEPARATOR)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

        # ── Quadro Resumo ──
        pdf.section_title("RESUMO DO CONTRATO")

        pdf.set_fill_color(*_LIGHT_GRAY)
        rows = [
            ("Projeto:", project_name),
            ("Valor Total:", _format_brl(contract_value)),
            ("Valor por Extenso:", _extenso_brl(contract_value)),
            ("Inicio:", _format_date(start_date)),
            ("Termino:", _format_date(end_date)),
            ("Numero:", contract_number),
        ]
        for label, value in rows:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*_DEEP_INDIGO)
            pdf.cell(45, 7, label, border=1, fill=True, **_RT)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*_BLACK)
            pdf.cell(145, 7, value[:60], border=1, **_NL)
        pdf.ln(5)

        # ── Clausulas ──
        pdf.section_title("CLAUSULAS CONTRATUAIS")

        # Clausula 1 — Objeto
        pdf.clause_header("PRIMEIRA", "DO OBJETO")
        pdf.clause_body(
            f"O presente contrato tem por objeto a prestacao de servicos de "
            f"marketing digital e tecnologia pela CONTRATADA em favor da CONTRATANTE, "
            f"conforme especificado no projeto \"{project_name}\", incluindo, mas nao "
            f"se limitando a: estrategia digital, gestao de trafego pago, criacao de "
            f"conteudo, desenvolvimento web e consultoria de posicionamento de marca."
        )

        # Clausula 2 — Valor e Pagamento
        pdf.clause_header("SEGUNDA", "DO VALOR E FORMA DE PAGAMENTO")
        pdf.clause_body(
            f"Pela prestacao dos servicos descritos na Clausula Primeira, a CONTRATANTE "
            f"pagara a CONTRATADA o valor total de {_format_brl(contract_value)} "
            f"({_extenso_brl(contract_value)}), podendo ser parcelado conforme acordo "
            f"entre as partes. O pagamento sera realizado via transferencia bancaria ou "
            f"PIX ate o 5o dia util de cada periodo contratual."
        )

        # Clausula 3 — Prazo
        pdf.clause_header("TERCEIRA", "DO PRAZO")
        pdf.clause_body(
            f"O presente contrato tera vigencia de {_format_date(start_date)} a "
            f"{_format_date(end_date)}, podendo ser renovado por acordo mutuo entre "
            f"as partes, mediante aditivo contratual assinado com antecedencia minima "
            f"de 15 (quinze) dias do termino."
        )

        # Clausula 4 — Obrigacoes da Contratada
        pdf.clause_header("QUARTA", "DAS OBRIGACOES DA CONTRATADA")
        pdf.clause_body(
            "A CONTRATADA se obriga a:\n"
            "a) Executar os servicos com diligencia e qualidade profissional;\n"
            "b) Apresentar relatorios mensais de performance;\n"
            "c) Manter sigilo sobre informacoes confidenciais da CONTRATANTE;\n"
            "d) Cumprir os prazos estabelecidos no cronograma do projeto."
        )

        # Clausula 5 — Obrigacoes da Contratante
        pdf.clause_header("QUINTA", "DAS OBRIGACOES DA CONTRATANTE")
        pdf.clause_body(
            "A CONTRATANTE se obriga a:\n"
            "a) Fornecer acesso e informacoes necessarias para a execucao dos servicos;\n"
            "b) Realizar os pagamentos nas datas pactuadas;\n"
            "c) Aprovar entregas dentro do prazo de 5 dias uteis;\n"
            "d) Designar um responsavel para comunicacao com a CONTRATADA."
        )

        # Clausula 6 — Rescisao
        pdf.clause_header("SEXTA", "DA RESCISAO")
        pdf.clause_body(
            "O presente contrato podera ser rescindido por qualquer das partes, "
            "mediante comunicacao formal com antecedencia minima de 30 (trinta) dias. "
            "Em caso de rescisao antecipada pela CONTRATANTE, sera devido o pagamento "
            "proporcional aos servicos ja executados."
        )

        # Clausula 7 — Confidencialidade
        pdf.clause_header("SETIMA", "DA CONFIDENCIALIDADE")
        pdf.clause_body(
            "As partes se comprometem a manter em sigilo todas as informacoes "
            "confidenciais trocadas durante a vigencia deste contrato, incluindo "
            "dados de clientes, estrategias de marketing, metricas de performance "
            "e propriedade intelectual, pelo prazo de 2 (dois) anos apos o termino."
        )

        # Clausula 8 — Foro
        pdf.clause_header("OITAVA", "DO FORO")
        pdf.clause_body(
            "As partes elegem o foro da comarca de [CIDADE/ESTADO] para dirimir "
            "quaisquer controversias oriundas do presente contrato, com renuncia "
            "expressa a qualquer outro, por mais privilegiado que seja."
        )

        pdf.ln(8)

        # ── Assinaturas ──
        pdf.section_title("ASSINATURAS")
        pdf.ln(4)

        y_sig = pdf.get_y()

        # Contratada
        pdf.set_xy(15, y_sig + 15)
        pdf.set_draw_color(*_DEEP_INDIGO)
        pdf.line(15, y_sig + 15, 95, y_sig + 15)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*_DEEP_INDIGO)
        pdf.cell(80, 6, "CONTRATADA", border=0, align="C", **_NL)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*_GRAY_TEXT)
        pdf.set_x(15)
        pdf.cell(80, 5, "Vyron System Tecnologia", border=0, align="C", **_NL)

        # Contratante
        pdf.set_xy(115, y_sig + 15)
        pdf.line(115, y_sig + 15, 195, y_sig + 15)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*_DEEP_INDIGO)
        pdf.cell(80, 6, "CONTRATANTE", border=0, align="C", **_NL)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*_GRAY_TEXT)
        pdf.set_x(115)
        pdf.cell(80, 5, client_name, border=0, align="C", **_NL)

        pdf.ln(6)

        # Data
        pdf.set_xy(10, pdf.get_y() + 4)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*_BLACK)
        now = datetime.now()
        pdf.cell(
            0, 6,
            f"[CIDADE], {now.day} de {_month_name(now.month)} de {now.year}.",
            border=0, align="C", **_NL,
        )

        # 3. Gerar bytes
        pdf_bytes = pdf.output()

        # 4. Persistir registro Contract no DB
        try:
            contract = models.Contract(
                id=uuid4(),
                client_id=client.id if client else None,
                project_id=project.id,
                contract_number=contract_number,
                content_html=f"Contrato {contract_number} gerado em PDF",
                variables_used={
                    "client_name": client_name,
                    "project_name": project_name,
                    "contract_value": contract_value,
                    "start_date": _format_date(start_date),
                    "end_date": _format_date(end_date),
                },
                status="draft",
                start_date=start_date,
                end_date=end_date,
                generated_at=now,
            )
            db.add(contract)
            db.commit()
        except Exception:
            db.rollback()  # Nao deve quebrar a geracao do PDF

        return pdf_bytes, contract_number


def _month_name(month: int) -> str:
    """Retorna nome do mes em portugues (latin-1 safe)."""
    names = {
        1: "janeiro", 2: "fevereiro", 3: "marco", 4: "abril",
        5: "maio", 6: "junho", 7: "julho", 8: "agosto",
        9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
    }
    return names.get(month, "???")

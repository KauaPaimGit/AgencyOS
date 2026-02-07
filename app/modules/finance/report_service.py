"""
Finance Report Service v1.1.1
=============================
Gerador de Relatorios Executivos em PDF para o Vyron System.

Utiliza fpdf2 com suporte a Latin-1 (acentuacao tratada),
design corporativo com cards de KPI, tabelas zebradas e footer
com rastreabilidade de auditoria.

Autor: Vyron System Engine
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from sqlalchemy.orm import Session

from app import models


# ============================================================
# CONSTANTES DE DESIGN
# ============================================================
_BLUE_DARK = (20, 30, 70)
_BLUE_ACCENT = (31, 119, 180)
_GREEN_DARK = (0, 100, 0)
_GREEN_LIGHT = (230, 245, 230)
_RED_DARK = (180, 0, 0)
_RED_LIGHT = (255, 240, 240)
_BLUE_LIGHT = (240, 245, 255)
_GRAY_HEADER = (220, 220, 220)
_GRAY_TEXT = (100, 100, 100)
_WHITE = (255, 255, 255)
_BLACK = (0, 0, 0)

_PROJECT_TYPE_LABELS: Dict[str, str] = {
    "recurring": "Recorrente",
    "one_off": "Pontual",
    "prospection": "Prospeccao",
}


# ============================================================
# FUNCOES AUXILIARES (NoneType-safe)
# ============================================================
def _safe_str(value: Any, fallback: str = "N/A") -> str:
    """Converte qualquer valor para string segura para Latin-1 (fpdf2)."""
    if value is None:
        return fallback
    text = str(value)
    return text.encode("latin-1", "replace").decode("latin-1")


def _safe_decimal(value: Any) -> Decimal:
    """Retorna Decimal seguro, tratando None e tipos inesperados."""
    if value is None:
        return Decimal("0")
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def _format_brl(value: Any) -> str:
    """Formata valor como moeda BRL."""
    v = float(_safe_decimal(value))
    return f"R$ {v:,.2f}"


def _format_pct(value: Any) -> str:
    """Formata valor como percentual."""
    v = float(_safe_decimal(value))
    return f"{v:.1f}%"


# ---- helpers de movimentacao ----
# ln=0 (old) => RIGHT / TOP  — cursor fica a direita da celula
# ln=1 (old) => LMARGIN / NEXT — cursor vai para inicio da proxima linha
_NL = {"new_x": XPos.LMARGIN, "new_y": YPos.NEXT}   # next line
_RT = {"new_x": XPos.RIGHT,   "new_y": YPos.TOP}     # right / same line


# ============================================================
# CLASSE PDF CORPORATIVA
# ============================================================
class VyronPDF(FPDF):
    """PDF customizado com header/footer corporativo Vyron System."""

    def __init__(self, project_name: str = "", project_type: str = ""):
        super().__init__()
        self._project_name = _safe_str(project_name, "Projeto")
        self._project_type = _PROJECT_TYPE_LABELS.get(
            project_type, _safe_str(project_type, "N/A")
        )

    def header(self):
        # Barra azul escura no topo
        self.set_fill_color(*_BLUE_DARK)
        self.rect(0, 0, 210, 22, "F")

        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*_WHITE)
        self.set_y(4)
        self.cell(
            0, 8, "VYRON SYSTEM  |  Relatorio Executivo",
            border=0, align="C", **_NL,
        )

        # Sub-header com projeto e tipo
        self.set_font("Helvetica", "", 9)
        self.set_text_color(200, 210, 240)
        label = f"{self._project_name}  [{self._project_type}]"
        self.cell(0, 6, label, border=0, align="C", **_NL)
        self.ln(4)

    def footer(self):
        self.set_y(-18)
        self.set_draw_color(180, 180, 180)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())

        self.set_y(-14)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*_GRAY_TEXT)
        ts = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(95, 10, f"Gerado em {ts} | Vyron System v1.1.1",
                  border=0, align="L", **_RT)
        self.cell(95, 10, f"Pagina {self.page_no()}/{{nb}}",
                  border=0, align="R", **_RT)

    # ----- helpers de layout -----
    def section_title(self, title: str, color: tuple = _BLUE_ACCENT):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*color)
        self.cell(0, 10, title, border=0, align="L", **_NL)
        self.ln(1)

    def kpi_card(self, x: float, y: float, w: float, h: float,
                 label: str, value: str, bg: tuple, label_color: tuple):
        self.set_fill_color(*bg)
        self.rect(x, y, w, h, "F")

        # Borda sutil
        self.set_draw_color(200, 200, 200)
        self.rect(x, y, w, h, "D")

        self.set_xy(x, y + 4)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*label_color)
        self.cell(w, 5, label, border=0, align="C", **_NL)

        self.set_xy(x, y + 12)
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*_BLACK)
        self.cell(w, 8, value, border=0, align="C", **_NL)


# ============================================================
# SERVICE PRINCIPAL
# ============================================================
class FinanceReportService:
    """
    Servico de geracao de relatorios financeiros em PDF.

    Consolida dados de Project, Revenue e Expense do banco,
    calcula KPIs e gera um PDF executivo pronto para download.
    """

    @staticmethod
    def generate(db: Session, project_id: str) -> bytes:
        """
        Gera o relatorio executivo financeiro de um projeto.

        Args:
            db: Sessao SQLAlchemy
            project_id: UUID do projeto (str)

        Returns:
            bytes do PDF gerado

        Raises:
            ValueError: projeto nao encontrado
            RuntimeError: erro na geracao do PDF
        """
        # -- 1. Buscar dados --
        project = (
            db.query(models.Project)
            .filter(models.Project.id == project_id)
            .first()
        )
        if not project:
            raise ValueError(f"Projeto {project_id} nao encontrado")

        revenues: List[models.Revenue] = (
            db.query(models.Revenue)
            .filter(models.Revenue.project_id == project_id)
            .order_by(models.Revenue.created_at.desc())
            .all()
        )
        expenses: List[models.Expense] = (
            db.query(models.Expense)
            .filter(models.Expense.project_id == project_id)
            .order_by(models.Expense.created_at.desc())
            .all()
        )

        # -- 2. Calculos financeiros (NoneType-safe) --
        total_revenue = sum(
            (_safe_decimal(r.amount) for r in revenues), Decimal("0")
        )
        total_expense = sum(
            (_safe_decimal(e.amount) for e in expenses), Decimal("0")
        )
        net_profit = total_revenue - total_expense
        margin = (
            (net_profit / total_revenue * 100)
            if total_revenue > 0
            else Decimal("0")
        )

        product_price = _safe_decimal(
            getattr(project, "product_price", None)
        )
        roi = Decimal("0")
        if product_price > 0 and total_expense > 0:
            estimated_rev = product_price * Decimal("10")
            roi = (estimated_rev - total_expense) / total_expense * 100

        # -- 3. Montar PDF --
        project_type_str = _safe_str(getattr(project, "type", None), "N/A")
        pdf = VyronPDF(
            project_name=_safe_str(project.name),
            project_type=project_type_str,
        )
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=20)

        # -- 4. Cards de KPI --
        pdf.section_title("INDICADORES DE PERFORMANCE", _BLUE_DARK)
        cw, ch, sp = 58, 26, 5
        sx = 15
        sy = pdf.get_y()

        pdf.kpi_card(sx, sy, cw, ch,
                     "RECEITA TOTAL", _format_brl(total_revenue),
                     _GREEN_LIGHT, _GREEN_DARK)
        pdf.kpi_card(sx + cw + sp, sy, cw, ch,
                     "DESPESAS TOTAIS", _format_brl(total_expense),
                     _RED_LIGHT, _RED_DARK)
        pdf.kpi_card(sx + (cw + sp) * 2, sy, cw, ch,
                     "LUCRO LIQUIDO", _format_brl(net_profit),
                     _BLUE_LIGHT, _BLUE_ACCENT)

        pdf.set_xy(10, sy + ch + 8)

        # -- 5. Informacoes do Projeto --
        pdf.section_title("INFORMACOES DO PROJETO")
        pdf.set_font("Helvetica", "B", 10)

        client_name = "N/A"
        if hasattr(project, "client") and project.client:
            client_name = _safe_str(project.client.name)

        start_dt = "N/A"
        if project.start_date:
            start_dt = project.start_date.strftime("%d/%m/%Y")

        end_dt = "N/A"
        if project.end_date:
            end_dt = project.end_date.strftime("%d/%m/%Y")

        type_label = _PROJECT_TYPE_LABELS.get(
            project_type_str, _safe_str(project_type_str)
        )

        info_rows = [
            ("Projeto:", _safe_str(project.name)),
            ("Cliente:", client_name),
            ("Tipo:", type_label),
            ("Status:", _safe_str(getattr(project, "status", "N/A")).upper()),
            ("Inicio:", start_dt),
            ("Termino:", end_dt),
            ("Valor Contrato:", _format_brl(getattr(project, "contract_value", 0))),
        ]

        for label, value in info_rows:
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_fill_color(*_GRAY_HEADER)
            pdf.set_text_color(*_BLACK)
            pdf.cell(55, 8, label, border=1, align="L", fill=True, **_RT)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(135, 8, value[:50], border=1, align="L", **_NL)

        pdf.ln(6)

        # -- 6. Resumo Financeiro --
        pdf.section_title("RESUMO FINANCEIRO", _GREEN_DARK)

        # Header da tabela
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(*_GRAY_HEADER)
        pdf.set_text_color(*_BLACK)
        pdf.cell(100, 8, "Metrica", border=1, align="L", fill=True, **_RT)
        pdf.cell(90, 8, "Valor", border=1, align="R", fill=True, **_NL)

        fin_rows = [
            ("Receita Total", _format_brl(total_revenue), False),
            ("Despesas Totais", _format_brl(total_expense), False),
            ("Lucro Liquido", _format_brl(net_profit), True),
            ("Margem de Lucro", _format_pct(margin), False),
        ]
        if roi != 0:
            fin_rows.append(("ROI Estimado", _format_pct(roi), False))

        for i, (metric, value, highlight) in enumerate(fin_rows):
            if highlight:
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_fill_color(200, 230, 200)
            else:
                pdf.set_font("Helvetica", "", 10)
                bg = (248, 248, 248) if i % 2 == 0 else _WHITE
                pdf.set_fill_color(*bg)
            pdf.set_text_color(*_BLACK)
            pdf.cell(100, 8, metric, border=1, align="L", fill=True, **_RT)
            pdf.cell(90, 8, value, border=1, align="R", fill=True, **_NL)

        pdf.ln(6)

        # -- 7. Detalhamento de Despesas --
        pdf.section_title("DETALHAMENTO DE DESPESAS", _RED_DARK)

        if expenses:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(*_GRAY_HEADER)
            pdf.set_text_color(*_BLACK)
            pdf.cell(22, 7, "Data", border=1, align="C", fill=True, **_RT)
            pdf.cell(85, 7, "Descricao", border=1, align="C", fill=True, **_RT)
            pdf.cell(35, 7, "Categoria", border=1, align="C", fill=True, **_RT)
            pdf.cell(22, 7, "Status", border=1, align="C", fill=True, **_RT)
            pdf.cell(26, 7, "Valor (R$)", border=1, align="C", fill=True, **_NL)

            pdf.set_font("Helvetica", "", 8)
            for i, exp in enumerate(expenses):
                bg = (248, 248, 248) if i % 2 == 0 else _WHITE
                pdf.set_fill_color(*bg)
                pdf.set_text_color(*_BLACK)

                dt = exp.due_date.strftime("%d/%m/%y") if exp.due_date else "N/A"
                desc = _safe_str(exp.description, "-")
                desc = desc[:32] + "..." if len(desc) > 32 else desc
                cat = _safe_str(exp.category, "Outros")[:15]
                status = _safe_str(getattr(exp, "status", ""), "-")[:10]
                amt = f"{float(_safe_decimal(exp.amount)):,.2f}"

                pdf.cell(22, 6, dt, border=1, align="C", fill=True, **_RT)
                pdf.cell(85, 6, desc, border=1, align="L", fill=True, **_RT)
                pdf.cell(35, 6, cat, border=1, align="C", fill=True, **_RT)
                pdf.cell(22, 6, status, border=1, align="C", fill=True, **_RT)
                pdf.cell(26, 6, amt, border=1, align="R", fill=True, **_NL)

            # Linha total
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(255, 200, 200)
            pdf.cell(164, 7, "TOTAL DE DESPESAS:", border=1,
                     align="R", fill=True, **_RT)
            pdf.cell(26, 7, f"{float(total_expense):,.2f}", border=1,
                     align="R", fill=True, **_NL)
        else:
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(*_GRAY_TEXT)
            pdf.cell(
                0, 8,
                "Nenhuma despesa registrada para este projeto.",
                border=0, align="C", **_NL,
            )

        pdf.ln(6)

        # -- 8. Detalhamento de Receitas --
        pdf.section_title("DETALHAMENTO DE RECEITAS", _GREEN_DARK)

        if revenues:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(*_GRAY_HEADER)
            pdf.set_text_color(*_BLACK)
            pdf.cell(22, 7, "Data", border=1, align="C", fill=True, **_RT)
            pdf.cell(90, 7, "Descricao", border=1, align="C", fill=True, **_RT)
            pdf.cell(40, 7, "Status", border=1, align="C", fill=True, **_RT)
            pdf.cell(38, 7, "Valor (R$)", border=1, align="C", fill=True, **_NL)

            pdf.set_font("Helvetica", "", 8)
            for i, rev in enumerate(revenues):
                bg = (248, 248, 248) if i % 2 == 0 else _WHITE
                pdf.set_fill_color(*bg)
                pdf.set_text_color(*_BLACK)

                dt = "N/A"
                paid_date = getattr(rev, "paid_date", None)
                if paid_date:
                    dt = paid_date.strftime("%d/%m/%y")
                else:
                    due_date = getattr(rev, "due_date", None)
                    if due_date:
                        dt = due_date.strftime("%d/%m/%y")

                desc = _safe_str(rev.description, "-")
                desc = desc[:38] + "..." if len(desc) > 38 else desc
                status = _safe_str(getattr(rev, "status", ""), "-")[:15]
                amt = f"{float(_safe_decimal(rev.amount)):,.2f}"

                pdf.cell(22, 6, dt, border=1, align="C", fill=True, **_RT)
                pdf.cell(90, 6, desc, border=1, align="L", fill=True, **_RT)
                pdf.cell(40, 6, status, border=1, align="C", fill=True, **_RT)
                pdf.cell(38, 6, amt, border=1, align="R", fill=True, **_NL)

            # Linha total
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(200, 230, 200)
            pdf.cell(152, 7, "TOTAL DE RECEITAS:", border=1,
                     align="R", fill=True, **_RT)
            pdf.cell(38, 7, f"{float(total_revenue):,.2f}", border=1,
                     align="R", fill=True, **_NL)
        else:
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(*_GRAY_TEXT)
            pdf.cell(
                0, 8,
                "Nenhuma receita registrada para este projeto.",
                border=0, align="C", **_NL,
            )

        pdf.ln(8)

        # -- 9. Selo de auditoria --
        pdf.set_font("Helvetica", "I", 7)
        pdf.set_text_color(*_GRAY_TEXT)
        pdf.cell(
            0, 5,
            "Documento gerado automaticamente pelo Vyron System. "
            "Dados sujeitos a auditoria e rastreabilidade.",
            border=0, align="C", **_NL,
        )

        # -- 10. Output --
        try:
            raw = pdf.output()  # fpdf2 >= 2.2: returns bytearray
            if isinstance(raw, bytearray):
                return bytes(raw)
            if isinstance(raw, str):
                return raw.encode("latin-1")
            return raw  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Falha ao renderizar PDF: {e}")

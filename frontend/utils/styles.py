"""
Vyron System v1.2 — Custom Styles (Dark HiTech Theme)

Paleta institucional:
  Dark Slate   #171923  — Fundo principal / Sidebar
  Deep Indigo  #2D3748  — Cards, Containers, Inputs
  Vivid Violet #7000FF  — Botões, Destaques, Bordas de foco
  Ice Blue     #A0AEC0  — Textos secundários, Labels
  White        #FFFFFF  — Valores numéricos e Títulos

Chamada: from app.utils.styles import apply_custom_styles
         apply_custom_styles()  # logo após st.set_page_config
"""
import streamlit as st

_DARK_SLATE = "#171923"
_DEEP_INDIGO = "#2D3748"
_VIVID_VIOLET = "#7000FF"
_VIOLET_GLOW = "#9B40FF"
_ICE_BLUE = "#A0AEC0"
_WHITE = "#FFFFFF"
_LIGHT_SLATE = "#E2E8F0"
_CARD_SHADOW = "0 2px 12px rgba(112,0,255,.15)"


def apply_custom_styles() -> None:
    """Injeta CSS customizado completo no Streamlit."""
    st.markdown(f"""
<style>
/* ══════════════════════════════════════════════════════════
   VYRON SYSTEM v1.2 — DARK HITECH THEME
   ══════════════════════════════════════════════════════════ */

/* ── Reset & Base ──────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {{
    background-color: {_DARK_SLATE};
    color: {_LIGHT_SLATE};
}}

/* ── Sidebar ───────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background-color: {_DARK_SLATE};
    border-right: 1px solid {_DEEP_INDIGO};
}}

[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {{
    background-color: {_DEEP_INDIGO};
    border: 1px solid {_DEEP_INDIGO};
    border-radius: 8px;
    color: {_LIGHT_SLATE};
    transition: border-color .2s;
}}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div:focus-within {{
    border-color: {_VIVID_VIOLET};
    box-shadow: 0 0 0 2px rgba(112,0,255,.25);
}}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:first-child {{
    color: {_WHITE};
}}

/* ── Headers globais ───────────────────────────────────── */
.main-header {{
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, {_VIVID_VIOLET}, {_VIOLET_GLOW});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: .6rem;
    letter-spacing: -.02em;
}}

.section-hdr {{
    font-size: 1.1rem;
    font-weight: 600;
    color: {_ICE_BLUE};
    margin: 0 0 .3rem 0;
}}

.block-label {{
    font-size: .85rem;
    color: {_ICE_BLUE};
    letter-spacing: .05rem;
    text-transform: uppercase;
}}

.sidebar-block-title {{
    font-size: .75rem;
    color: {_ICE_BLUE};
    letter-spacing: .12rem;
    text-transform: uppercase;
    margin: 1.2rem 0 .3rem .2rem;
}}

/* ── Metric Cards (st.metric) ──────────────────────────── */
[data-testid="stMetric"] {{
    background: {_DEEP_INDIGO};
    border-left: 3px solid {_VIVID_VIOLET};
    border-radius: 8px;
    padding: 1rem 1.2rem;
    box-shadow: {_CARD_SHADOW};
    transition: transform .15s, box-shadow .15s;
}}
[data-testid="stMetric"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(112,0,255,.25);
}}

/* Label (Receita, ROI, etc) */
[data-testid="stMetric"] label,
[data-testid="stMetric"] [data-testid="stMetricLabel"] {{
    color: {_ICE_BLUE} !important;
    font-size: .85rem;
    font-weight: 500;
    letter-spacing: .03em;
}}

/* Valor numérico */
[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: {_WHITE} !important;
    font-size: 1.6rem;
    font-weight: 700;
}}

/* Delta (variação) */
[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
    font-size: .8rem;
}}

/* ── Containers / Cards ────────────────────────────────── */
[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {_DEEP_INDIGO};
    border: 1px solid rgba(112,0,255,.2);
    border-left: 3px solid {_VIVID_VIOLET};
    border-radius: 10px;
    box-shadow: {_CARD_SHADOW};
    padding: .2rem;
}}

/* ── Inputs (Text, Number, Select) ─────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div,
[data-testid="stDateInput"] input,
textarea {{
    background-color: {_DEEP_INDIGO} !important;
    border: 1px solid rgba(160,174,192,.25) !important;
    border-radius: 8px !important;
    color: {_LIGHT_SLATE} !important;
    transition: border-color .2s, box-shadow .2s;
}}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
textarea:focus {{
    border-color: {_VIVID_VIOLET} !important;
    box-shadow: 0 0 0 2px rgba(112,0,255,.3) !important;
}}

/* ── Botões ────────────────────────────────────────────── */
/* Primários (st.button type="primary") */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"],
.stDownloadButton > button {{
    background: linear-gradient(135deg, {_VIVID_VIOLET}, {_VIOLET_GLOW}) !important;
    color: {_WHITE} !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    letter-spacing: .02em;
    box-shadow: 0 2px 8px rgba(112,0,255,.3);
    transition: all .2s ease;
}}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover,
.stDownloadButton > button:hover {{
    box-shadow: 0 0 20px rgba(112,0,255,.5), 0 0 40px rgba(112,0,255,.2) !important;
    transform: translateY(-1px);
    filter: brightness(1.1);
}}

/* Secundários */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"] {{
    background: {_DEEP_INDIGO} !important;
    color: {_LIGHT_SLATE} !important;
    border: 1px solid rgba(112,0,255,.35) !important;
    border-radius: 8px !important;
    transition: all .2s ease;
}}
.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="stBaseButton-secondary"]:hover {{
    border-color: {_VIVID_VIOLET} !important;
    box-shadow: 0 0 12px rgba(112,0,255,.3) !important;
    color: {_WHITE} !important;
}}

/* ── Expanders ─────────────────────────────────────────── */
[data-testid="stExpander"] {{
    background: {_DEEP_INDIGO};
    border: 1px solid rgba(112,0,255,.15);
    border-radius: 10px;
}}
[data-testid="stExpander"] summary {{
    color: {_LIGHT_SLATE};
    font-weight: 600;
}}
[data-testid="stExpander"] summary:hover {{
    color: {_VIVID_VIOLET};
}}

/* ── Tabs ──────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background: {_DEEP_INDIGO};
    border-radius: 10px;
    padding: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    color: {_ICE_BLUE};
    font-weight: 500;
    padding: 8px 20px;
}}
.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background: {_VIVID_VIOLET};
    color: {_WHITE};
}}
.stTabs [data-baseweb="tab-highlight"] {{
    background: {_VIVID_VIOLET};
    border-radius: 8px;
}}

/* ── Dataframes / Tables ───────────────────────────────── */
[data-testid="stDataFrame"],
[data-testid="stTable"] {{
    border-radius: 8px;
    overflow: hidden;
}}

/* ── Alerts ────────────────────────────────────────────── */
.stAlert {{
    border-radius: 8px;
    border-left: 3px solid {_VIVID_VIOLET};
}}

/* ── Info / Success / Warning / Error ──────────────────── */
[data-testid="stNotification"] {{
    border-radius: 8px;
}}

/* ── Plotly charts background ──────────────────────────── */
.js-plotly-plot .plotly .main-svg {{
    background: transparent !important;
}}

/* ── Scrollbar ─────────────────────────────────────────── */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}
::-webkit-scrollbar-track {{
    background: {_DARK_SLATE};
}}
::-webkit-scrollbar-thumb {{
    background: {_DEEP_INDIGO};
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: {_VIVID_VIOLET};
}}

/* ── Health / Status badge ─────────────────────────────── */
[data-testid="stSidebar"] .stSuccess {{
    background: rgba(112,0,255,.1);
    border-left-color: {_VIVID_VIOLET};
    border-radius: 8px;
}}

/* ── Dividers ──────────────────────────────────────────── */
hr {{
    border-color: rgba(112,0,255,.12) !important;
}}

/* ── Download link override (Excel export etc) ─────────── */
a[download] {{
    color: {_VIVID_VIOLET} !important;
    font-weight: 600;
    text-decoration: none;
    transition: color .2s;
}}
a[download]:hover {{
    color: {_VIOLET_GLOW} !important;
    text-shadow: 0 0 8px rgba(112,0,255,.4);
}}

/* ── Forms ─────────────────────────────────────────────── */
[data-testid="stForm"] {{
    background: {_DEEP_INDIGO};
    border: 1px solid rgba(112,0,255,.15);
    border-radius: 10px;
    padding: 1.2rem;
}}

/* ── Sidebar info block (username/role) ────────────────── */
[data-testid="stSidebar"] [data-testid="stNotification"] {{
    background: rgba(112,0,255,.08);
    border-left: 3px solid {_VIVID_VIOLET};
    border-radius: 8px;
}}

/* ── Caption text ──────────────────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] {{
    color: {_ICE_BLUE} !important;
}}

/* ── Version badge at sidebar bottom ───────────────────── */
[data-testid="stSidebar"] .stCaption {{
    color: rgba(160,174,192,.6) !important;
}}
</style>
""", unsafe_allow_html=True)

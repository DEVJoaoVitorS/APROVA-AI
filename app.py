import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Anota AI | EVTL",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS PROFISSIONAL — ENGENHARIA / URBANISMO
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background-color: #F8F7F4 !important;
    color: #1A1A2E !important;
}

[data-testid="stSidebar"] {
    background-color: #1A1A2E !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: #E8E6E0 !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] h3 {
    color: #A8A5A0 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebar"] h3 {
    color: #F8F7F4 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    border-bottom: 1px solid #2E2E4E !important;
    padding-bottom: 8px !important;
    margin-top: 24px !important;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #1A1A2E !important;
}

/* HERO HEADER */
.hero-section {
    background: #1A1A2E;
    padding: 32px 40px;
    margin: -1rem -1rem 0 -1rem;
    border-bottom: 3px solid #C8A96E;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #F8F7F4;
    letter-spacing: -0.02em;
    margin: 0;
}

.hero-subtitle {
    font-size: 14px;
    color: #A8A5A0;
    margin-top: 4px;
    letter-spacing: 0.05em;
}

.hero-accent {
    color: #C8A96E;
}

/* KPI CARDS */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E8E6E0;
    border-top: 3px solid #1A1A2E;
    padding: 20px 24px;
    border-radius: 4px;
    margin-bottom: 12px;
}

.kpi-card.approved {
    border-top-color: #2D6A4F;
}

.kpi-card.warning {
    border-top-color: #C8A96E;
}

.kpi-card.danger {
    border-top-color: #C0392B;
}

.kpi-label {
    font-size: 10px;
    font-weight: 700;
    color: #888580;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.kpi-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #1A1A2E;
    line-height: 1;
}

.kpi-sub {
    font-size: 12px;
    color: #888580;
    margin-top: 4px;
}

/* STATUS BANNER */
.status-aprovado {
    background: #F0FAF5;
    border-left: 4px solid #2D6A4F;
    padding: 16px 20px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.status-reprovado {
    background: #FEF5F5;
    border-left: 4px solid #C0392B;
    padding: 16px 20px;
    margin-bottom: 24px;
}

.status-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 4px;
}

.status-aprovado .status-title { color: #2D6A4F; }
.status-reprovado .status-title { color: #C0392B; }
.status-body { font-size: 13px; color: #555; }

/* SECTION LABELS */
.section-label {
    font-size: 10px;
    font-weight: 700;
    color: #888580;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 6px 0;
    border-bottom: 1px solid #E8E6E0;
    margin-bottom: 16px;
}

/* TABLE */
.param-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
.param-table th {
    background: #1A1A2E;
    color: #F8F7F4;
    padding: 10px 14px;
    text-align: left;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.param-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #E8E6E0;
    color: #333;
}
.param-table tr:last-child td { border-bottom: none; }
.param-table tr:hover td { background: #F8F7F4; }
.param-value {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    color: #1A1A2E;
}
.param-ok { color: #2D6A4F; font-weight: 700; }
.param-fail { color: #C0392B; font-weight: 700; }

/* ROI SECTION */
.roi-box {
    background: #1A1A2E;
    color: #F8F7F4;
    padding: 24px 28px;
    border-radius: 4px;
    margin-top: 16px;
}
.roi-big {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px;
    font-weight: 700;
    color: #C8A96E;
    line-height: 1;
}
.roi-label {
    font-size: 12px;
    color: #A8A5A0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* BUTTONS */
.stButton > button {
    background: #1A1A2E !important;
    color: #F8F7F4 !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 10px 20px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background: #2E2E4E !important;
}
.stDownloadButton > button {
    background: #2D6A4F !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid #E8E6E0 !important;
    background: transparent !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #888580 !important;
    padding: 12px 20px !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    color: #1A1A2E !important;
    border-bottom: 2px solid #C8A96E !important;
    background: transparent !important;
}

/* DIVIDER */
hr { border-color: #E8E6E0 !important; }

/* INFO BOXES */
.info-box {
    background: #FFFBF4;
    border: 1px solid #F0E6CC;
    border-left: 3px solid #C8A96E;
    padding: 12px 16px;
    border-radius: 3px;
    font-size: 13px;
    color: #555;
    margin: 12px 0;
}

/* Inputs sidebar */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #252545 !important;
    border-color: #3A3A5E !important;
    color: #E8E6E0 !important;
}
[data-testid="stSidebar"] .stNumberInput > div > div > input {
    background: #252545 !important;
    border-color: #3A3A5E !important;
    color: #E8E6E0 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. DADOS REAIS DE ZONEAMENTO
#    Fontes: Lei Complementar 449/2024 - Itajaí
#            Lei de Uso e Ocupação do Solo - Navegantes
# ==========================================

zonas_data = {
    # ---- ITAJAÍ (Lei Complementar nº 449/2024) ----
    "Itajaí — ZMC1 (Zona Mista Central 1)": {
        "municipio": "Itajaí",
        "lei": "LC 449/2024 — Art. 71",
        "CA_basico": 5.0,
        "CA_total": 8.5,
        "CA_outorga": 3.5,
        "TO_base": 0.80,
        "TO_torre": 0.60,
        "Gabarito_ref": "Varia por largura da via (até 105m)",
        "Gabarito_m": 67.4,
        "Recuo_Frontal": 4.0,
        "Recuo_Lateral": 0.0,
        "Permeabilidade": 0.10,
        "Lote_Minimo": 200,
        "Testada_Minima": 10.0,
        "Profundidade_Min": 20.0,
        "Fator_contribuicao": 0.30,
        "descricao": "Centralidade metropolitana, centro histórico e orla fluvial. Estimula compactação habitacional com comércio no térreo.",
    },
    "Itajaí — ZMC2 (Zona Mista Central 2)": {
        "municipio": "Itajaí",
        "lei": "LC 449/2024 — Art. 72",
        "CA_basico": 4.0,
        "CA_total": 7.5,
        "CA_outorga": 3.0,
        "TO_base": 0.80,
        "TO_torre": 0.60,
        "Gabarito_ref": "Varia por largura da via",
        "Gabarito_m": 67.4,
        "Recuo_Frontal": 4.0,
        "Recuo_Lateral": 0.0,
        "Permeabilidade": 0.10,
        "Lote_Minimo": 200,
        "Testada_Minima": 10.0,
        "Profundidade_Min": 20.0,
        "Fator_contribuicao": 0.20,
        "descricao": "Extensão oeste do núcleo histórico. Mix residencial/comercial com fachadas ativas.",
    },
    "Itajaí — ZMC3 (Zona Mista Central 3)": {
        "municipio": "Itajaí",
        "lei": "LC 449/2024 — Art. 73",
        "CA_basico": 3.5,
        "CA_total": 6.5,
        "CA_outorga": 2.5,
        "TO_base": 0.80,
        "TO_torre": 0.60,
        "Gabarito_ref": "Varia por largura da via",
        "Gabarito_m": 67.4,
        "Recuo_Frontal": 4.0,
        "Recuo_Lateral": 0.0,
        "Permeabilidade": 0.10,
        "Lote_Minimo": 200,
        "Testada_Minima": 10.0,
        "Profundidade_Min": 20.0,
        "Fator_contribuicao": 0.15,
        "descricao": "Eixos de crescimento linear. Centralidades ao longo de vias conectoras.",
    },
    "Itajaí — ZMR (Zona Mista Residencial)": {
        "municipio": "Itajaí",
        "lei": "LC 449/2024 — Art. 74",
        "CA_basico": 3.0,
        "CA_total": 6.0,
        "CA_outorga": 1.5,
        "TO_base": 0.80,
        "TO_torre": 0.60,
        "Gabarito_ref": "Varia por largura da via",
        "Gabarito_m": 37.4,
        "Recuo_Frontal": 4.0,
        "Recuo_Lateral": 0.0,
        "Permeabilidade": 0.10,
        "Lote_Minimo": 200,
        "Testada_Minima": 10.0,
        "Profundidade_Min": 20.0,
        "Fator_contribuicao": 0.10,
        "descricao": "Adensamento habitacional com mescla de usos. Embasamentos menores que nas ZMCs.",
    },
    "Itajaí — ZRP1 (Zona Residencial Predominante 1)": {
        "municipio": "Itajaí",
        "lei": "LC 449/2024 — Art. 75",
        "CA_basico": 2.5,
        "CA_total": 5.5,
        "CA_outorga": 0.0,
        "TO_base": 0.80,
        "TO_torre": 0.60,
        "Gabarito_ref": "12,80m + ático",
        "Gabarito_m": 12.8,
        "Recuo_Frontal": 4.0,
        "Recuo_Lateral": 1.5,
        "Permeabilidade": 0.15,
        "Lote_Minimo": 200,
        "Testada_Minima": 10.0,
        "Profundidade_Min": 20.0,
        "Fator_contribuicao": 0.0,
        "descricao": "Predomínio habitacional. Correlação com moradias unifamiliares. Usos mistos e fachadas ativas estimulados.",
    },
    "Itajaí — ZRP2 (Zona Residencial Predominante 2)": {
        "municipio": "Itajaí",
        "lei": "LC 449/2024 — Art. 76",
        "CA_basico": 1.0,
        "CA_total": 4.0,
        "CA_outorga": 0.0,
        "TO_base": 0.80,
        "TO_torre": 0.60,
        "Gabarito_ref": "7,40m + ático",
        "Gabarito_m": 7.4,
        "Recuo_Frontal": 4.0,
        "Recuo_Lateral": 1.5,
        "Permeabilidade": 0.20,
        "Lote_Minimo": 200,
        "Testada_Minima": 10.0,
        "Profundidade_Min": 20.0,
        "Fator_contribuicao": 0.0,
        "descricao": "Predomínio habitacional mais restritivo. Correlação maior com moradias unifamiliares.",
    },
    "Itajaí — ZI (Zona Industrial)": {
        "municipio": "Itajaí",
        "lei": "LC 449/2024 — Art. 77",
        "CA_basico": 1.0,
        "CA_total": 3.0,
        "CA_outorga": 2.0,
        "TO_base": 0.80,
        "TO_torre": 0.60,
        "Gabarito_ref": "32m uso comercial / 7,40m + ático uso habitacional",
        "Gabarito_m": 32.0,
        "Recuo_Frontal": 0.0,
        "Recuo_Lateral": 2.5,
        "Permeabilidade": 0.10,
        "Lote_Minimo": 200,
        "Testada_Minima": 20.0,
        "Profundidade_Min": 50.0,
        "Fator_contribuicao": 0.10,
        "descricao": "Transformação/armazenagem de produtos. Eixos rodoviários. Uso residencial permitido até 250m².",
    },
    "Itajaí — ZBR (Zona Beira Rio)": {
        "municipio": "Itajaí",
        "lei": "LC 449/2024 — Art. 82",
        "CA_basico": 1.5,
        "CA_total": 6.0,
        "CA_outorga": 0.0,
        "TO_base": 1.00,
        "TO_torre": 0.70,
        "Gabarito_ref": "16,40m / 22,40m (§3º)",
        "Gabarito_m": 16.4,
        "Recuo_Frontal": 0.0,
        "Recuo_Lateral": 0.0,
        "Permeabilidade": 0.10,
        "Lote_Minimo": 200,
        "Testada_Minima": 10.0,
        "Profundidade_Min": 20.0,
        "Fator_contribuicao": 0.0,
        "descricao": "Contato centro/Foz Itajaí. Lazer, gastronomia e hotelaria. Sem exigência de vagas de estacionamento.",
    },
    "Itajaí — ZTU1 (Zona de Transição Urbanística 1)": {
        "municipio": "Itajaí",
        "lei": "LC 449/2024 — Art. 84",
        "CA_basico": 3.0,
        "CA_total": 4.0,
        "CA_outorga": 1.0,
        "TO_base": 0.70,
        "TO_torre": 0.40,
        "Gabarito_ref": "43,4m + ático",
        "Gabarito_m": 43.4,
        "Recuo_Frontal": 5.0,
        "Recuo_Lateral": 2.5,
        "Permeabilidade": 0.25,
        "Lote_Minimo": 300,
        "Testada_Minima": 15.0,
        "Profundidade_Min": 30.0,
        "Fator_contribuicao": 0.20,
        "descricao": "Transição entre áreas urbanas e preservação. Alturas limitadas para valorizar visualização da morraria.",
    },
    "Itajaí — ZTU3 (Zona de Transição Urbanística 3)": {
        "municipio": "Itajaí",
        "lei": "LC 449/2024 — Art. 86",
        "CA_basico": 3.5,
        "CA_total": 4.5,
        "CA_outorga": 1.0,
        "TO_base": 0.60,
        "TO_torre": 0.50,
        "Gabarito_ref": "52,90m + ático",
        "Gabarito_m": 52.9,
        "Recuo_Frontal": 5.0,
        "Recuo_Lateral": 2.5,
        "Permeabilidade": 0.10,
        "Lote_Minimo": 300,
        "Testada_Minima": 15.0,
        "Profundidade_Min": 30.0,
        "Fator_contribuicao": 0.20,
        "descricao": "Transição urbana/preservação ao longo do Rio Itajaí-Mirim. Transferência de índices estimulada.",
    },
    # ---- NAVEGANTES (Lei de Uso e Ocupação do Solo) ----
    "Navegantes — ZR1 (Zona Residencial 1)": {
        "municipio": "Navegantes",
        "lei": "Lei de Uso e Ocupação do Solo — Navegantes",
        "CA_basico": 2.0,
        "CA_total": 2.0,
        "CA_outorga": 0.0,
        "TO_base": 0.60,
        "TO_torre": 0.60,
        "Gabarito_ref": "15m",
        "Gabarito_m": 15.0,
        "Recuo_Frontal": 4.0,
        "Recuo_Lateral": 1.5,
        "Permeabilidade": 0.20,
        "Lote_Minimo": 300,
        "Testada_Minima": 12.0,
        "Profundidade_Min": 25.0,
        "Fator_contribuicao": 0.0,
        "descricao": "Zona residencial de baixa densidade. Uso predominantemente unifamiliar.",
    },
    "Navegantes — ZCC (Zona Comercial Central)": {
        "municipio": "Navegantes",
        "lei": "Lei de Uso e Ocupação do Solo — Navegantes",
        "CA_basico": 4.0,
        "CA_total": 4.0,
        "CA_outorga": 0.0,
        "TO_base": 0.80,
        "TO_torre": 0.80,
        "Gabarito_ref": "30m",
        "Gabarito_m": 30.0,
        "Recuo_Frontal": 3.0,
        "Recuo_Lateral": 0.0,
        "Permeabilidade": 0.10,
        "Lote_Minimo": 250,
        "Testada_Minima": 10.0,
        "Profundidade_Min": 20.0,
        "Fator_contribuicao": 0.0,
        "descricao": "Centro comercial. Alta densidade, recuos reduzidos, gabarito maior.",
    },
    "Navegantes — ZR2 (Zona Residencial 2)": {
        "municipio": "Navegantes",
        "lei": "Lei de Uso e Ocupação do Solo — Navegantes",
        "CA_basico": 3.0,
        "CA_total": 3.0,
        "CA_outorga": 0.0,
        "TO_base": 0.65,
        "TO_torre": 0.65,
        "Gabarito_ref": "20m",
        "Gabarito_m": 20.0,
        "Recuo_Frontal": 4.0,
        "Recuo_Lateral": 1.5,
        "Permeabilidade": 0.15,
        "Lote_Minimo": 250,
        "Testada_Minima": 10.0,
        "Profundidade_Min": 20.0,
        "Fator_contribuicao": 0.0,
        "descricao": "Zona residencial de média densidade. Mix residencial/serviços vicinais.",
    },
    "Navegantes — ZI (Zona Industrial)": {
        "municipio": "Navegantes",
        "lei": "Lei de Uso e Ocupação do Solo — Navegantes",
        "CA_basico": 2.0,
        "CA_total": 2.0,
        "CA_outorga": 0.0,
        "TO_base": 0.70,
        "TO_torre": 0.70,
        "Gabarito_ref": "20m",
        "Gabarito_m": 20.0,
        "Recuo_Frontal": 5.0,
        "Recuo_Lateral": 3.0,
        "Permeabilidade": 0.20,
        "Lote_Minimo": 1000,
        "Testada_Minima": 20.0,
        "Profundidade_Min": 40.0,
        "Fator_contribuicao": 0.0,
        "descricao": "Atividades industriais e logísticas. Adjacências ao porto de Navegantes.",
    },
}

# ==========================================
# 4. SIDEBAR — INPUTS
# ==========================================
with st.sidebar:
    st.markdown("<h3>📍 Município & Zona</h3>", unsafe_allow_html=True)

    municipio_sel = st.selectbox(
        "MUNICÍPIO",
        ["Itajaí", "Navegantes"],
        help="Selecione o município do imóvel"
    )

    zonas_filtradas = {k: v for k, v in zonas_data.items() if v["municipio"] == municipio_sel}
    zona_sel = st.selectbox(
        "ZONEAMENTO",
        list(zonas_filtradas.keys()),
        help="Zona conforme legislação municipal vigente"
    )

    st.markdown("<h3>📐 Geometria do Lote</h3>", unsafe_allow_html=True)

    largura = st.number_input("TESTADA (m)", min_value=1.0, value=12.0, step=0.5, help="Frente do lote para via pública")
    comprimento = st.number_input("PROFUNDIDADE (m)", min_value=1.0, value=25.0, step=0.5)

    st.markdown("<h3>💰 Parâmetros Comerciais</h3>", unsafe_allow_html=True)

    tamanho_medio_apt = st.number_input("ÁREA MÉDIA POR UNID. (m²)", min_value=20.0, value=65.0, step=1.0)
    preco_venda_m2 = st.number_input("PREÇO DE VENDA (R$/m²)", min_value=1000.0, value=8500.0, step=500.0)
    custo_construcao_m2 = st.number_input("CUSTO CONSTRUÇÃO (R$/m²)", min_value=500.0, value=3200.0, step=100.0, help="CUB referência SC")

    st.markdown("<h3>📊 Análise de ROI</h3>", unsafe_allow_html=True)
    tempo_manual_h = st.number_input("HORAS PARA ANÁLISE MANUAL", min_value=1.0, value=12.0, step=1.0, help="Horas que levaria sem a ferramenta")
    custo_hora = st.number_input("CUSTO HORA-HOMEM (R$)", min_value=10.0, value=150.0, step=10.0)
    investimento_ia = st.number_input("INVESTIMENTO FERRAMENTA (R$)", min_value=0.0, value=500.0, step=100.0, help="Custo mensal ou por projeto")

# ==========================================
# 5. MOTOR DE CÁLCULO
# ==========================================
regras = zonas_data[zona_sel]
area_terreno = largura * comprimento

erros = []
avisos = []

if area_terreno < regras["Lote_Minimo"]:
    erros.append(f"Área do lote ({area_terreno:.0f} m²) inferior ao mínimo legal ({regras['Lote_Minimo']:.0f} m²).")
if largura < regras["Testada_Minima"]:
    erros.append(f"Testada ({largura:.1f} m) inferior ao mínimo legal ({regras['Testada_Minima']:.1f} m).")
if comprimento < regras["Profundidade_Min"]:
    erros.append(f"Profundidade ({comprimento:.1f} m) inferior ao mínimo recomendado ({regras['Profundidade_Min']:.1f} m).")

if regras["Permeabilidade"] > 0.15:
    avisos.append(f"Taxa de permeabilidade elevada ({regras['Permeabilidade']*100:.0f}%). Considere permeabilidade induzida (+20%).")

aprovado = len(erros) == 0

if aprovado:
    area_max_computavel = area_terreno * regras["CA_total"]
    area_basica = area_terreno * regras["CA_basico"]
    area_outorga = area_terreno * regras["CA_outorga"]
    area_ocupada_base = area_terreno * regras["TO_base"]
    area_livre = area_terreno - area_ocupada_base
    unidades_estimadas = max(1, int(area_max_computavel / tamanho_medio_apt))
    vgv_estimado = area_max_computavel * preco_venda_m2
    custo_obra = area_max_computavel * custo_construcao_m2
    margem_bruta = vgv_estimado - custo_obra
    margem_pct = (margem_bruta / vgv_estimado * 100) if vgv_estimado > 0 else 0

    # Outorga onerosa estimada
    CUB_SC = 2850  # CUB médio SC (referência)
    outorga_estimada = regras["Fator_contribuicao"] * CUB_SC * area_outorga if area_outorga > 0 else 0
else:
    area_max_computavel = area_basica = area_outorga = area_ocupada_base = area_livre = 0
    unidades_estimadas = vgv_estimado = custo_obra = margem_bruta = margem_pct = outorga_estimada = 0

# ROI da ferramenta
tempo_ia_h = 0.1  # ~6 minutos
roi_formula = ((tempo_manual_h - tempo_ia_h) * custo_hora - investimento_ia) / max(investimento_ia, 1) * 100
economia_por_uso = (tempo_manual_h - tempo_ia_h) * custo_hora

# ==========================================
# 6. HEADER PRINCIPAL
# ==========================================
st.markdown("""
<div class="hero-section">
    <div class="hero-title">ANOTA AI <span class="hero-accent">·</span> EVTL</div>
    <div class="hero-subtitle">ESTUDO DE VIABILIDADE TÉCNICA E LEGAL — VALE DO ITAJAÍ · SC</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 7. ABAS PRINCIPAIS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "  Resumo Executivo  ",
    "  Modelagem 3D  ",
    "  Parâmetros Legais  ",
    "  ROI & Impacto  "
])

# ==========================================
# TAB 1 — RESUMO EXECUTIVO
# ==========================================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    # Status Banner
    if aprovado:
        st.markdown(f"""
        <div class="status-aprovado">
            <div>
                <div class="status-title">✓ Conformidade Verificada</div>
                <div class="status-body">
                    {zona_sel.split('—')[1].strip()} · {regras['municipio']} ·
                    Análise baseada em {regras['lei']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        erros_html = "".join([f"<li style='margin-bottom:6px'>{e}</li>" for e in erros])
        st.markdown(f"""
        <div class="status-reprovado">
            <div class="status-title">✗ Parâmetros Incompatíveis — Revisão Necessária</div>
            <ul style='margin-top:10px; padding-left:20px; font-size:13px; color:#555;'>
                {erros_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    if avisos:
        for av in avisos:
            st.markdown(f'<div class="info-box">⚠ {av}</div>', unsafe_allow_html=True)

    if aprovado:
        # KPI Row 1
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Área do Terreno</div>
                <div class="kpi-value">{area_terreno:,.0f}</div>
                <div class="kpi-sub">metros quadrados</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="kpi-card approved">
                <div class="kpi-label">Potencial Construtivo Total</div>
                <div class="kpi-value">{area_max_computavel:,.0f}</div>
                <div class="kpi-sub">m² · CA {regras['CA_total']:.1f}x</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Unidades Estimadas</div>
                <div class="kpi-value">{unidades_estimadas}</div>
                <div class="kpi-sub">aptos de {tamanho_medio_apt:.0f} m² médios</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="kpi-card warning">
                <div class="kpi-label">VGV Estimado</div>
                <div class="kpi-value">R$ {vgv_estimado/1_000_000:.2f}M</div>
                <div class="kpi-sub">a R$ {preco_venda_m2:,.0f}/m²</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # KPI Row 2
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Área Básica (sem outorga)</div>
                <div class="kpi-value">{area_basica:,.0f}</div>
                <div class="kpi-sub">m² · CA básico {regras['CA_basico']:.1f}x</div>
            </div>""", unsafe_allow_html=True)
        with col6:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Custo Estimado de Obra</div>
                <div class="kpi-value">R$ {custo_obra/1_000_000:.2f}M</div>
                <div class="kpi-sub">a R$ {custo_construcao_m2:,.0f}/m²</div>
            </div>""", unsafe_allow_html=True)
        with col7:
            cor_margem = "approved" if margem_pct > 20 else ("warning" if margem_pct > 10 else "danger")
            st.markdown(f"""
            <div class="kpi-card {cor_margem}">
                <div class="kpi-label">Margem Bruta Estimada</div>
                <div class="kpi-value">{margem_pct:.1f}%</div>
                <div class="kpi-sub">R$ {margem_bruta/1_000_000:.2f}M</div>
            </div>""", unsafe_allow_html=True)
        with col8:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Outorga Onerosa Est.</div>
                <div class="kpi-value">R$ {outorga_estimada/1_000:.0f}K</div>
                <div class="kpi-sub">FC {regras['Fator_contribuicao']:.2f} · CUB SC ref.</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts
        col_g1, col_g2 = st.columns([1, 1])

        with col_g1:
            st.markdown('<div class="section-label">Distribuição do Solo</div>', unsafe_allow_html=True)
            fig_donut = go.Figure(data=[go.Pie(
                labels=['Área Ocupável (base)', 'Área Livre / Permeável'],
                values=[area_ocupada_base, area_livre],
                hole=0.65,
                marker_colors=['#1A1A2E', '#C8A96E'],
                textinfo='label+percent',
                textfont=dict(size=12, family='Inter'),
                hovertemplate='<b>%{label}</b><br>%{value:.0f} m²<extra></extra>'
            )])
            fig_donut.add_annotation(
                text=f"<b>{area_terreno:.0f}</b><br>m² total",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, family='Space Grotesk', color='#1A1A2E')
            )
            fig_donut.update_layout(
                margin=dict(l=10, r=10, b=10, t=10),
                height=260,
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                legend=dict(orientation='h', y=-0.1, font=dict(size=11, family='Inter'))
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        with col_g2:
            st.markdown('<div class="section-label">Potencial Construtivo por Tipo</div>', unsafe_allow_html=True)
            labels = ['CA Básico (livre)', 'CA Outorga (pago)', 'Não Aproveitável']
            values = [area_basica, area_outorga, 0]
            soma = area_basica + area_outorga
            nao_utilizado = max(0, area_max_computavel - soma)
            values[-1] = nao_utilizado

            fig_bar = go.Figure(go.Bar(
                x=labels,
                y=values,
                marker_color=['#2D6A4F', '#C8A96E', '#E8E6E0'],
                text=[f'{v:,.0f} m²' for v in values],
                textposition='outside',
                textfont=dict(size=11, family='Space Grotesk')
            ))
            fig_bar.update_layout(
                margin=dict(l=10, r=10, b=10, t=10),
                height=260,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(showgrid=True, gridcolor='#E8E6E0', tickfont=dict(size=10)),
                xaxis=dict(tickfont=dict(size=11, family='Inter')),
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # PDF Export
        st.markdown('<div class="section-label">Exportar Laudo</div>', unsafe_allow_html=True)

        def gerar_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_margins(20, 20, 20)

            # HEADER
            pdf.set_fill_color(26, 26, 46)
            pdf.rect(0, 0, 210, 35, 'F')
            pdf.set_font("Helvetica", 'B', 18)
            pdf.set_text_color(248, 247, 244)
            pdf.set_xy(20, 10)
            pdf.cell(0, 10, "ANOTA AI | EVTL", ln=False)
            pdf.set_font("Helvetica", '', 10)
            pdf.set_text_color(168, 165, 160)
            pdf.set_xy(20, 22)
            pdf.cell(0, 8, "Estudo de Viabilidade Tecnica e Legal", ln=True)

            # Linha dourada
            pdf.set_fill_color(200, 169, 110)
            pdf.rect(0, 35, 210, 2, 'F')

            pdf.set_xy(20, 45)
            pdf.set_text_color(26, 26, 46)
            pdf.set_font("Helvetica", 'B', 13)
            pdf.cell(0, 8, "1. IDENTIFICACAO DO ATIVO", ln=True)

            pdf.set_font("Helvetica", '', 11)
            pdf.set_fill_color(248, 247, 244)
            dados = [
                ("Municipio", regras["municipio"]),
                ("Zoneamento", zona_sel.split("—")[1].strip()[:60]),
                ("Legislacao", regras["lei"][:60]),
                ("Data da Analise", datetime.now().strftime("%d/%m/%Y %H:%M")),
                ("Testada", f"{largura:.1f} m"),
                ("Profundidade", f"{comprimento:.1f} m"),
                ("Area Total do Lote", f"{area_terreno:.2f} m2"),
            ]
            for label, valor in dados:
                pdf.set_xy(20, pdf.get_y())
                pdf.set_font("Helvetica", 'B', 10)
                pdf.set_text_color(136, 133, 128)
                pdf.cell(65, 7, label.upper(), ln=False)
                pdf.set_font("Helvetica", '', 11)
                pdf.set_text_color(26, 26, 46)
                pdf.cell(0, 7, str(valor), ln=True)

            pdf.ln(4)
            pdf.set_font("Helvetica", 'B', 13)
            pdf.set_text_color(26, 26, 46)
            pdf.cell(0, 8, "2. PARAMETROS URBANISTICOS (LEGAIS)", ln=True)

            params = [
                ("Coef. Aproveit. Basico", f"{regras['CA_basico']:.1f}x"),
                ("Coef. Aproveit. Total (c/ outorga)", f"{regras['CA_total']:.1f}x"),
                ("Taxa de Ocupacao Base", f"{regras['TO_base']*100:.0f}%"),
                ("Taxa de Ocupacao Torre", f"{regras['TO_torre']*100:.0f}%"),
                ("Permeabilidade Minima", f"{regras['Permeabilidade']*100:.0f}%"),
                ("Recuo Frontal", f"{regras['Recuo_Frontal']:.1f} m"),
                ("Recuo Lateral/Fundos", f"{regras['Recuo_Lateral']:.1f} m (embasamento)"),
                ("Altura Maxima Referencia", regras['Gabarito_ref']),
                ("Lote Minimo", f"{regras['Lote_Minimo']:.0f} m2"),
                ("Testada Minima", f"{regras['Testada_Minima']:.1f} m"),
            ]
            for label, valor in params:
                pdf.set_xy(20, pdf.get_y())
                pdf.set_font("Helvetica", 'B', 10)
                pdf.set_text_color(136, 133, 128)
                pdf.cell(80, 7, label.upper(), ln=False)
                pdf.set_font("Helvetica", '', 11)
                pdf.set_text_color(26, 26, 46)
                pdf.cell(0, 7, str(valor), ln=True)

            pdf.ln(4)
            pdf.set_font("Helvetica", 'B', 13)
            pdf.set_text_color(26, 26, 46)
            pdf.cell(0, 8, "3. STATUS DE CONFORMIDADE", ln=True)

            if aprovado:
                pdf.set_fill_color(240, 250, 245)
                pdf.set_draw_color(45, 106, 79)
                pdf.set_text_color(45, 106, 79)
                pdf.set_font("Helvetica", 'B', 12)
                pdf.set_xy(20, pdf.get_y())
                pdf.cell(170, 10, "  APROVADO — PARAMETROS EM CONFORMIDADE", border=1, fill=True, ln=True, align='C')
            else:
                pdf.set_fill_color(254, 245, 245)
                pdf.set_draw_color(192, 57, 43)
                pdf.set_text_color(192, 57, 43)
                pdf.set_font("Helvetica", 'B', 12)
                pdf.set_xy(20, pdf.get_y())
                pdf.cell(170, 10, "  REPROVADO — REVISAO NECESSARIA", border=1, fill=True, ln=True, align='C')
                pdf.set_font("Helvetica", '', 10)
                pdf.set_text_color(80, 80, 80)
                for err in erros:
                    pdf.set_xy(25, pdf.get_y() + 2)
                    pdf.cell(0, 6, f"• {err[:95]}", ln=True)

            if aprovado:
                pdf.ln(4)
                pdf.set_text_color(26, 26, 46)
                pdf.set_font("Helvetica", 'B', 13)
                pdf.cell(0, 8, "4. POTENCIAL CONSTRUTIVO E INDICADORES", ln=True)

                indicadores = [
                    ("Area Maxima Computavel (CA Total)", f"{area_max_computavel:,.0f} m2"),
                    ("Area Basica (CA Basico — sem outorga)", f"{area_basica:,.0f} m2"),
                    ("Area via Outorga Onerosa", f"{area_outorga:,.0f} m2"),
                    ("Unidades Estimadas", f"{unidades_estimadas} unidades de {tamanho_medio_apt:.0f} m2"),
                    ("VGV Estimado", f"R$ {vgv_estimado:,.2f}"),
                    ("Custo Estimado de Obra", f"R$ {custo_obra:,.2f}"),
                    ("Margem Bruta Estimada", f"{margem_pct:.1f}% (R$ {margem_bruta:,.2f})"),
                    ("Outorga Onerosa Estimada", f"R$ {outorga_estimada:,.2f}"),
                ]
                for label, valor in indicadores:
                    pdf.set_xy(20, pdf.get_y())
                    pdf.set_font("Helvetica", 'B', 10)
                    pdf.set_text_color(136, 133, 128)
                    pdf.cell(90, 7, label.upper(), ln=False)
                    pdf.set_font("Helvetica", '', 11)
                    pdf.set_text_color(26, 26, 46)
                    pdf.cell(0, 7, str(valor), ln=True)

            # ROI
            pdf.ln(4)
            pdf.set_font("Helvetica", 'B', 13)
            pdf.set_text_color(26, 26, 46)
            pdf.cell(0, 8, "5. ANALISE DE ROI DA FERRAMENTA", ln=True)
            pdf.set_font("Helvetica", '', 10)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(170, 6,
                f"Formula: ROI = (TEMPO_manual - TEMPO_ia) x CUSTO_hora / INVESTIMENTO_ia\n"
                f"ROI = ({tempo_manual_h:.1f}h - {tempo_ia_h:.1f}h) x R$ {custo_hora:.0f} / R$ {investimento_ia:.0f}\n"
                f"ROI = {roi_formula:.1f}%  |  Economia por uso: R$ {economia_por_uso:,.2f}"
            )

            # FOOTER
            pdf.set_fill_color(26, 26, 46)
            pdf.rect(0, 282, 210, 15, 'F')
            pdf.set_xy(20, 285)
            pdf.set_font("Helvetica", '', 8)
            pdf.set_text_color(168, 165, 160)
            pdf.cell(0, 6, f"Anota AI EVTL  |  Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}  |  Dados baseados em legislacao vigente. Verificar Plano Diretor vigente antes de protocolo.", ln=False)

            return pdf.output(dest='S').encode('latin-1')

        col_dl, col_info = st.columns([1, 2])
        with col_dl:
            pdf_bytes = gerar_pdf()
            st.download_button(
                "⬇ Baixar Laudo PDF",
                data=pdf_bytes,
                file_name=f"EVTL_{regras['municipio']}_{zona_sel.split('—')[1].strip()[:20].replace(' ','_')}.pdf",
                mime="application/pdf"
            )
        with col_info:
            st.markdown(f'<div class="info-box">Laudo gerado conforme <b>{regras["lei"]}</b>. Verificar Plano Diretor e legislação vigente antes de protocolo junto à Prefeitura.</div>', unsafe_allow_html=True)


# ==========================================
# TAB 2 — MODELAGEM 3D
# ==========================================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    if not aprovado:
        st.markdown("""
        <div class="status-reprovado">
            <div class="status-title">✗ Renderização Indisponível</div>
            <div class="status-body">Corrija as incompatibilidades para visualizar o envelope construtivo.</div>
        </div>""", unsafe_allow_html=True)
    else:
        col_info3d, _ = st.columns([3, 1])
        with col_info3d:
            st.markdown('<div class="section-label">Envelope Construtivo Máximo</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="info-box">
                Visualização do envelope máximo permitido na {zona_sel.split("—")[1].strip()}.
                Altura de referência: <b>{regras['Gabarito_ref']}</b>.
                O modelo considera recuos frontais ({regras['Recuo_Frontal']:.1f}m) e laterais ({regras['Recuo_Lateral']:.1f}m).
            </div>""", unsafe_allow_html=True)

        # Cálculo do envelope com recuos
        x0 = regras["Recuo_Lateral"]
        x1 = largura - regras["Recuo_Lateral"]
        y0 = regras["Recuo_Frontal"]
        y1 = comprimento - regras["Recuo_Frontal"]
        z_max = min(regras["Gabarito_m"], 80)  # limita para visualização
        z_emb = min(regras.get("Gabarito_m", 12) * 0.4, 16.4)

        # Terreno (plano base)
        terreno = go.Mesh3d(
            x=[0, 0, largura, largura],
            y=[0, comprimento, comprimento, 0],
            z=[0, 0, 0, 0],
            i=[0, 0], j=[1, 2], k=[2, 3],
            opacity=0.15,
            color='#C8A96E',
            name='Terreno',
            showlegend=True
        )

        # Envelope (embasamento)
        def cubo_mesh3d(x0, x1, y0, y1, z0, z1, color, opacity, name):
            vx = [x0, x0, x1, x1, x0, x0, x1, x1]
            vy = [y0, y1, y1, y0, y0, y1, y1, y0]
            vz = [z0, z0, z0, z0, z1, z1, z1, z1]
            i_ = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
            j_ = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
            k_ = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
            return go.Mesh3d(x=vx, y=vy, z=vz, i=i_, j=j_, k=k_,
                             opacity=opacity, color=color, name=name, showlegend=True)

        envelope_emb = cubo_mesh3d(x0, x1, y0, y1, 0, z_emb, '#1A1A2E', 0.35, 'Embasamento')
        envelope_torre = cubo_mesh3d(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, z_emb, z_max, '#2D6A4F', 0.25, 'Torre máxima')

        fig_3d = go.Figure(data=[terreno, envelope_emb, envelope_torre])
        fig_3d.update_layout(
            scene=dict(
                xaxis=dict(title='Testada (m)', backgroundcolor="#F8F7F4",
                           gridcolor="#E8E6E0", color="#1A1A2E", tickfont=dict(size=9)),
                yaxis=dict(title='Profundidade (m)', backgroundcolor="#F8F7F4",
                           gridcolor="#E8E6E0", color="#1A1A2E", tickfont=dict(size=9)),
                zaxis=dict(title='Altura (m)', backgroundcolor="#F8F7F4",
                           gridcolor="#E8E6E0", color="#1A1A2E", tickfont=dict(size=9)),
                bgcolor="#F8F7F4",
                aspectmode='data',
                camera=dict(eye=dict(x=1.8, y=-1.8, z=1.2))
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='rgba(0,0,0,0)',
            height=520,
            legend=dict(x=0, y=1, font=dict(size=11, family='Inter'),
                        bgcolor='rgba(255,255,255,0.8)')
        )
        st.plotly_chart(fig_3d, use_container_width=True)

        # Dimensões resumidas
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        dims = [
            ("Projeção no térreo", f"{(x1-x0):.1f} × {(y1-y0):.1f} m"),
            ("Área ocupada base", f"{(x1-x0)*(y1-y0):,.0f} m²"),
            ("Altura embasamento", f"{z_emb:.1f} m"),
            ("Altura máxima ref.", f"{z_max:.1f} m"),
        ]
        for col, (lbl, val) in zip([col_d1, col_d2, col_d3, col_d4], dims):
            with col:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">{lbl}</div>
                    <div class="kpi-value" style="font-size:18px">{val}</div>
                </div>""", unsafe_allow_html=True)


# ==========================================
# TAB 3 — PARÂMETROS LEGAIS
# ==========================================
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Matriz Legislativa Completa</div>', unsafe_allow_html=True)

    def status_param(valor_real, minimo):
        ok = valor_real >= minimo
        icon = "✓" if ok else "✗"
        cls = "param-ok" if ok else "param-fail"
        return f'<span class="{cls}">{icon}</span>'

    linhas = [
        ("Área do Lote", f"{area_terreno:.0f} m²", f"{regras['Lote_Minimo']:.0f} m²",
         status_param(area_terreno, regras["Lote_Minimo"])),
        ("Testada", f"{largura:.1f} m", f"{regras['Testada_Minima']:.1f} m",
         status_param(largura, regras["Testada_Minima"])),
        ("Profundidade", f"{comprimento:.1f} m", f"{regras['Profundidade_Min']:.1f} m",
         status_param(comprimento, regras["Profundidade_Min"])),
        ("CA Básico", f"{regras['CA_basico']:.1f}x", "—", '<span class="param-ok">✓</span>'),
        ("CA Total (c/ outorga)", f"{regras['CA_total']:.1f}x", "—", '<span class="param-ok">✓</span>'),
        ("Taxa de Ocupação Base", f"{regras['TO_base']*100:.0f}%", "Máximo permitido", '<span class="param-ok">✓</span>'),
        ("Taxa de Ocupação Torre", f"{regras['TO_torre']*100:.0f}%", "Máximo permitido", '<span class="param-ok">✓</span>'),
        ("Taxa de Permeabilidade", f"{regras['Permeabilidade']*100:.0f}%", "Mínimo obrigatório", '<span class="param-ok">✓</span>'),
        ("Recuo Frontal (embasamento)", f"{regras['Recuo_Frontal']:.1f} m", "Mínimo", '<span class="param-ok">✓</span>'),
        ("Recuo Lateral/Fundos (embasamento)", f"{regras['Recuo_Lateral']:.1f} m", "Mínimo", '<span class="param-ok">✓</span>'),
        ("Gabarito de Referência", regras["Gabarito_ref"], "—", '<span class="param-ok">✓</span>'),
        ("Fator de Contribuição (outorga)", f"{regras['Fator_contribuicao']:.2f}", "—", '<span class="param-ok">✓</span>'),
    ]

    rows_html = ""
    for nome, atual, limite, status in linhas:
        rows_html += f"""
        <tr>
            <td>{nome}</td>
            <td><span class="param-value">{atual}</span></td>
            <td>{limite}</td>
            <td style="text-align:center">{status}</td>
        </tr>"""

    st.markdown(f"""
    <table class="param-table">
        <thead>
            <tr>
                <th>Parâmetro</th>
                <th>Valor / Limite Legal</th>
                <th>Referência</th>
                <th style="text-align:center">Status</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Descrição da Zona</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">📋 <b>{zona_sel}</b><br><br>{regras["descricao"]}<br><br><i>Fonte: {regras["lei"]}</i></div>', unsafe_allow_html=True)

    # Comparativo de zonas do mesmo município
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Comparativo de Zonas — {}</div>'.format(regras["municipio"]), unsafe_allow_html=True)

    zonas_mun = {k: v for k, v in zonas_data.items() if v["municipio"] == regras["municipio"]}
    comp_data = {
        "Zona": [k.split("—")[1].strip() for k in zonas_mun.keys()],
        "CA Básico": [v["CA_basico"] for v in zonas_mun.values()],
        "CA Total": [v["CA_total"] for v in zonas_mun.values()],
        "TO Base (%)": [v["TO_base"] * 100 for v in zonas_mun.values()],
        "Permeab. (%)": [v["Permeabilidade"] * 100 for v in zonas_mun.values()],
        "Lote Mín. (m²)": [v["Lote_Minimo"] for v in zonas_mun.values()],
    }
    df_comp = pd.DataFrame(comp_data)
    st.dataframe(
        df_comp.set_index("Zona"),
        use_container_width=True,
        height=250
    )


# ==========================================
# TAB 4 — ROI & IMPACTO
# ==========================================
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Análise de Retorno sobre Investimento (ROI)</div>', unsafe_allow_html=True)

    col_roi1, col_roi2 = st.columns([1, 1])

    with col_roi1:
        st.markdown(f"""
        <div class="roi-box">
            <div class="roi-label">ROI da Ferramenta</div>
            <div class="roi-big">{roi_formula:.0f}%</div>
            <div style="margin-top:16px; font-size:13px; color:#A8A5A0;">
                Fórmula aplicada:<br>
                <code style="color:#C8A96E; font-size:12px;">
                ROI = (T_manual − T_ia) × Custo_hora<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;────────────────────<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Investimento_IA
                </code>
            </div>
            <div style="margin-top:16px; border-top:1px solid #2E2E4E; padding-top:12px;">
                <div style="font-size:12px; color:#A8A5A0; margin-bottom:4px;">ECONOMIA POR USO</div>
                <div style="font-family:'Space Grotesk'; font-size:20px; font-weight:700; color:#C8A96E;">
                    R$ {economia_por_uso:,.2f}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_roi2:
        st.markdown('<div class="section-label">Decomposição do ROI</div>', unsafe_allow_html=True)
        kpis_roi = [
            ("Tempo análise manual", f"{tempo_manual_h:.1f} h"),
            ("Tempo com Anota AI", f"{tempo_ia_h:.1f} h (~6 min)"),
            ("Redução de tempo", f"{((tempo_manual_h - tempo_ia_h)/tempo_manual_h)*100:.0f}%"),
            ("Custo hora-homem", f"R$ {custo_hora:.0f}/h"),
            ("Custo por análise (manual)", f"R$ {tempo_manual_h * custo_hora:,.0f}"),
            ("Custo por análise (com IA)", f"R$ {tempo_ia_h * custo_hora:,.0f}"),
            ("Investimento na ferramenta", f"R$ {investimento_ia:,.0f}"),
            ("ROI resultante", f"{roi_formula:.1f}%"),
        ]
        for lbl, val in kpis_roi:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:7px 0; border-bottom:1px solid #E8E6E0; font-size:13px;">
                <span style="color:#888580">{lbl}</span>
                <span style="font-family:'Space Grotesk'; font-weight:600; color:#1A1A2E">{val}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Projeção de Ganho Acumulado por Volume de Análises</div>', unsafe_allow_html=True)

    usos = list(range(1, 31))
    ganho_acumulado = [max(0, (economia_por_uso * n) - investimento_ia) for n in usos]
    break_even = next((n for n, g in zip(usos, ganho_acumulado) if g > 0), None)

    fig_roi = go.Figure()
    fig_roi.add_trace(go.Scatter(
        x=usos, y=ganho_acumulado,
        fill='tozeroy', fillcolor='rgba(45, 106, 79, 0.1)',
        line=dict(color='#2D6A4F', width=2.5),
        name='Ganho líquido acumulado',
        hovertemplate='Análise nº%{x}<br>Ganho: R$ %{y:,.0f}<extra></extra>'
    ))
    if break_even:
        fig_roi.add_vline(
            x=break_even, line_dash="dash", line_color="#C8A96E",
            annotation_text=f"Break-even: análise {break_even}",
            annotation_font_size=11
        )
    fig_roi.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Número de análises', gridcolor='#E8E6E0', tickfont=dict(size=10)),
        yaxis=dict(title='Ganho líquido (R$)', gridcolor='#E8E6E0', tickfont=dict(size=10),
                   tickprefix='R$ ', tickformat=',.0f'),
        margin=dict(l=10, r=10, b=10, t=10),
        height=280,
        showlegend=False
    )
    st.plotly_chart(fig_roi, use_container_width=True)

    st.markdown('<div class="section-label">Proposta de Valor — Por que Anota AI?</div>', unsafe_allow_html=True)
    cols_v = st.columns(3)
    valores = [
        ("⏱ Velocidade", f"De {tempo_manual_h:.0f}h para 6 minutos por análise. Dados legislativos atualizados com as leis vigentes de Itajaí e Navegantes."),
        ("⚖ Confiabilidade", "Parâmetros extraídos diretamente das legislações oficiais: LC 449/2024 (Itajaí) e Lei de Uso e Ocupação do Solo (Navegantes)."),
        ("📈 Escalabilidade", "Uma ferramenta para engenheiros, incorporadores e prefeituras. Múltiplos cenários em segundos, com exportação de laudo profissional."),
    ]
    for col, (titulo, desc) in zip(cols_v, valores):
        with col:
            st.markdown(f"""
            <div class="kpi-card approved" style="padding:20px;">
                <div style="font-family:'Space Grotesk'; font-size:15px; font-weight:700; color:#1A1A2E; margin-bottom:10px;">{titulo}</div>
                <div style="font-size:13px; color:#555; line-height:1.5">{desc}</div>
            </div>""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Aprova AI | Estudo de Viabilidade", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# INJEÇÃO DE CSS CUSTOMIZADO (ESTÉTICA GO.ARCH)
# ==========================================
estilo_customizado = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif !important;
    }
    .stApp {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #333333 !important;
    }
    h1, h2, h3, h4 {
        color: #C5A059 !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    .stSelectbox div[data-baseweb="select"], .stNumberInput input {
        background-color: #222222 !important;
        border: 1px solid #C5A059 !important;
        color: #ffffff !important;
        border-radius: 0px !important;
    }
    .metric-box {
        background-color: #222222;
        padding: 20px;
        border-top: 3px solid #C5A059;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-title {
        font-size: 14px;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #C5A059;
        margin-top: 10px;
    }
    hr { border-color: #333333 !important; }
</style>
"""
st.markdown(estilo_customizado, unsafe_allow_html=True)

# ==========================================
# DADOS DE SIMULAÇÃO (MOCK DATA)
# Substituiremos pelos dados reais depois
# ==========================================
zonas_mock = {
    "ZR1 (Zona Residencial 1)": {"CA": 2.0, "TO": 0.60, "Gabarito": 15, "Recuo_Frontal": 4.0, "Recuo_Lateral": 1.5},
    "ZCC (Zona Comercial Central)": {"CA": 4.0, "TO": 0.80, "Gabarito": 30, "Recuo_Frontal": 3.0, "Recuo_Lateral": 0.0}
}

# ==========================================
# INTERFACE LATERAL (INPUTS DO TERRENO)
# ==========================================
st.sidebar.markdown("<h3>CONFIGURAÇÃO DO LOTE</h3>", unsafe_allow_html=True)

cidade = st.sidebar.selectbox("Município", ["Navegantes - SC"])
zona = st.sidebar.selectbox("Zoneamento", list(zonas_mock.keys()))

st.sidebar.markdown("---")
largura = st.sidebar.number_input("Largura do Terreno (m)", min_value=5.0, value=12.0, step=0.5)
comprimento = st.sidebar.number_input("Comprimento do Terreno (m)", min_value=10.0, value=25.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size: 12px; color: #a0a0a0;'>Estimativa Comercial</p>", unsafe_allow_html=True)
tamanho_medio_apt = st.sidebar.number_input("Tamanho Médio da Unidade (m²)", min_value=20.0, value=65.0, step=1.0)
preco_venda_m2 = st.sidebar.number_input("Preço de Venda Esperado (R$/m²)", min_value=1000.0, value=8500.0, step=500.0)

# ==========================================
# CÁLCULOS MATEMÁTICOS (O MOTOR DO EVTL)
# ==========================================
regras = zonas_mock[zona]
area_terreno = largura * comprimento
area_max_computavel = area_terreno * regras["CA"]
area_projecao_maxima = area_terreno * regras["TO"]

unidades_estimadas = int(area_max_computavel / tamanho_medio_apt)
vgv_estimado = area_max_computavel * preco_venda_m2

# ==========================================
# CABEÇALHO DO DASHBOARD
# ==========================================
st.title("APROVA AI")
st.markdown("<p style='font-size: 16px; color: #a0a0a0;'>ESTUDO DE VIABILIDADE TÉCNICA E LEGAL (EVTL)</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# LINHA 1: MÉTRICAS DE IMPACTO
# ==========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div class='metric-box'><div class='metric-title'>Área do Terreno</div><div class='metric-value'>{area_terreno:,.0f} m²</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-box'><div class='metric-title'>Potencial Construtivo (Máx)</div><div class='metric-value'>{area_max_computavel:,.0f} m²</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-box'><div class='metric-title'>Unidades Estimadas</div><div class='metric-value'>{unidades_estimadas}</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-box'><div class='metric-title'>VGV Estimado *</div><div class='metric-value'>R$ {vgv_estimado:,.2f}</div></div>", unsafe_allow_html=True)

st.markdown("<p style='font-size: 11px; color: #777; text-align: right;'>* O VGV é uma estimativa bruta baseada no potencial construtivo máximo x valor de venda preenchido, não substitui orçamento executivo.</p>", unsafe_allow_html=True)

# ==========================================
# LINHA 2: ENVELOPE 3D E DIRETRIZES
# ==========================================
st.markdown("---")
col_grafico, col_tabela = st.columns([1.5, 1])

with col_grafico:
    st.markdown("<h3>ENVELOPE VOLUMÉTRICO MÁXIMO</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; font-size: 14px;'>Visualização interativa baseada nos recuos e gabarito da zona.</p>", unsafe_allow_html=True)
    
    # Gerador do Gráfico 3D com Plotly
    # Coordenadas do bloco construtivo (descontando os recuos)
    x_inicio = regras["Recuo_Lateral"]
    x_fim = largura - regras["Recuo_Lateral"]
    y_inicio = regras["Recuo_Frontal"]
    y_fim = comprimento - regras["Recuo_Frontal"] # Assumindo recuo de fundo igual ao frontal por enquanto
    z_altura = regras["Gabarito"]

    # Desenhando o bloco
    fig = go.Figure(data=[
        go.Mesh3d(
            # 8 vértices do paralelepípedo
            x=[x_inicio, x_inicio, x_fim, x_fim, x_inicio, x_inicio, x_fim, x_fim],
            y=[y_inicio, y_fim, y_fim, y_inicio, y_inicio, y_fim, y_fim, y_inicio],
            z=[0, 0, 0, 0, z_altura, z_altura, z_altura, z_altura],
            i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            opacity=0.6,
            color='#C5A059',
            flatshading=True
        )
    ])

    # Desenhando a "base" do terreno (O lote todo)
    fig.add_trace(go.Mesh3d(
        x=[0, 0, largura, largura],
        y=[0, comprimento, comprimento, 0],
        z=[0, 0, 0, 0],
        i=[0, 0], j=[1, 2], k=[2, 3],
        opacity=0.2, color='#ffffff'
    ))

    # Estilizando o gráfico para ficar com fundo transparente e linhas escuras
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Largura (m)', range=[0, largura + 5], backgroundcolor="#111", gridcolor="#333"),
            yaxis=dict(title='Comprimento (m)', range=[0, comprimento + 5], backgroundcolor="#111", gridcolor="#333"),
            zaxis=dict(title='Altura Máx (m)', range=[0, z_altura + 10], backgroundcolor="#111", gridcolor="#333"),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

with col_tabela:
    st.markdown("<h3>PARÂMETROS DA ZONA</h3>", unsafe_allow_html=True)
    
    # Criando a tabela fixa de regras
    dados_tabela = {
        "DIRETRIZ URBANÍSTICA": [
            "Coeficiente de Aproveitamento (CA)", 
            "Taxa de Ocupação Máxima (TO)", 
            "Gabarito Máximo (Altura)", 
            "Recuo Frontal Obrigatório", 
            "Recuo Lateral / Fundos"
        ],
        "LIMITE LEGAL": [
            f"{regras['CA']}x a área do lote",
            f"{regras['TO']*100:.0f}%",
            f"{regras['Gabarito']} metros",
            f"{regras['Recuo_Frontal']} metros",
            f"{regras['Recuo_Lateral']} metros"
        ]
    }
    df_regras = pd.DataFrame(dados_tabela)
    st.table(df_regras)
    
    st.markdown("---")
    st.markdown("<h3>ÍNDICE DE APROVEITAMENTO</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #a0a0a0;'>A sua projeção térrea atual é de <strong>{area_projecao_maxima:,.0f} m²</strong>, atingindo 100% da Taxa de Ocupação máxima permitida para o térreo nesta zona.</p>", unsafe_allow_html=True)

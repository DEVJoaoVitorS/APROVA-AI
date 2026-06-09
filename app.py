import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Aprova AI | Dashboard EVTL", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# INJEÇÃO DE CSS (DESIGN PREMIUM - DASHBOARD)
# ==========================================
estilo_customizado = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif !important;
    }
    .stApp {
        background-color: #121212 !important; /* Fundo ainda mais escuro para destacar gráficos */
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #222222 !important;
    }
    h1, h2, h3, h4 {
        color: #C5A059 !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    
    /* Estilização das Abas (Tabs) para visual moderno */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #888888;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stTabs [aria-selected="true"] {
        color: #C5A059 !important;
        border-bottom: 2px solid #C5A059 !important;
    }
    
    .stSelectbox div[data-baseweb="select"], .stNumberInput input {
        background-color: #1a1a1a !important;
        border: 1px solid #C5A059 !important;
        color: #ffffff !important;
        border-radius: 0px !important;
    }
    .metric-box {
        background-color: #1a1a1a;
        padding: 24px;
        border-left: 4px solid #C5A059; /* Borda lateral elegante */
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-title {
        font-size: 13px;
        color: #888888;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #C5A059;
        margin-top: 8px;
    }
    hr { border-color: #222222 !important; }
</style>
"""
st.markdown(estilo_customizado, unsafe_allow_html=True)

# ==========================================
# DADOS DE SIMULAÇÃO (MOCK DATA)
# ==========================================
zonas_mock = {
    "ZR1 (Zona Residencial 1)": {"CA": 2.0, "TO": 0.60, "Gabarito": 15, "Recuo_Frontal": 4.0, "Recuo_Lateral": 1.5},
    "ZCC (Zona Comercial Central)": {"CA": 4.0, "TO": 0.80, "Gabarito": 30, "Recuo_Frontal": 3.0, "Recuo_Lateral": 0.0}
}

# ==========================================
# INTERFACE LATERAL (INPUTS DO TERRENO)
# ==========================================
st.sidebar.markdown("<h3>📍 LOCALIZAÇÃO</h3>", unsafe_allow_html=True)
cidade = st.sidebar.selectbox("Município", ["Navegantes - SC"])
zona = st.sidebar.selectbox("Zoneamento", list(zonas_mock.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("<h3>📐 DIMENSÕES DO LOTE</h3>", unsafe_allow_html=True)
largura = st.sidebar.number_input("Testada / Largura (m)", min_value=5.0, value=12.0, step=0.5)
comprimento = st.sidebar.number_input("Profundidade / Comprimento (m)", min_value=10.0, value=25.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.markdown("<h3>💰 PREMISSAS COMERCIAIS</h3>", unsafe_allow_html=True)
tamanho_medio_apt = st.sidebar.number_input("Tamanho Médio da Unidade (m²)", min_value=20.0, value=65.0, step=1.0)
preco_venda_m2 = st.sidebar.number_input("Preço de Venda Esperado (R$/m²)", min_value=1000.0, value=8500.0, step=500.0)

# ==========================================
# CÁLCULOS MATEMÁTICOS
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
st.markdown("<h1 style='font-size: 2.5rem; margin-bottom: 0;'>APROVA AI <span style='color: #555; font-weight: 300;'>| EVTL</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 14px; color: #888; margin-top: -10px;'>ESTUDO DE VIABILIDADE TÉCNICA E LEGAL AUTOMATIZADO</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# ESTRUTURA EM ABAS (NOVO DESIGN)
# ==========================================
tab1, tab2, tab3 = st.tabs(["📊 Resumo Executivo", "🏗️ Modelagem Volumétrica 3D", "⚖️ Parâmetros Legais"])

# ABA 1: RESUMO EXECUTIVO
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>Área do Terreno</div><div class='metric-value'>{area_terreno:,.0f} m²</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>Potencial Máx. (CA)</div><div class='metric-value'>{area_max_computavel:,.0f} m²</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>Unidades Estimadas</div><div class='metric-value'>{unidades_estimadas}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>VGV Estimado *</div><div class='metric-value'>R$ {vgv_estimado:,.0f}</div></div>", unsafe_allow_html=True)

    st.markdown("<p style='font-size: 11px; color: #555; text-align: right;'>* Estimativa bruta baseada no potencial construtivo máximo. Não substitui análise financeira executiva.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h3>🎯 INSIGHT DO TERRENO</h3>", unsafe_allow_html=True)
    st.info(f"O lote selecionado permite uma ocupação térrea máxima de **{area_projecao_maxima:,.0f} m²**. A verticalização é limitada ao gabarito de **{regras['Gabarito']} metros** de altura.")

# ABA 2: MODELAGEM 3D
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; font-size: 14px;'>Utilize o mouse para rotacionar o envelope volumétrico máximo permitido no lote.</p>", unsafe_allow_html=True)
    
    x_inicio = regras["Recuo_Lateral"]
    x_fim = largura - regras["Recuo_Lateral"]
    y_inicio = regras["Recuo_Frontal"]
    y_fim = comprimento - regras["Recuo_Frontal"]
    z_altura = regras["Gabarito"]

    fig = go.Figure(data=[
        go.Mesh3d(
            x=[x_inicio, x_inicio, x_fim, x_fim, x_inicio, x_inicio, x_fim, x_fim],
            y=[y_inicio, y_fim, y_fim, y_inicio, y_inicio, y_fim, y_fim, y_inicio],
            z=[0, 0, 0, 0, z_altura, z_altura, z_altura, z_altura],
            i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            opacity=0.7, color='#C5A059', flatshading=True
        )
    ])
    fig.add_trace(go.Mesh3d(
        x=[0, 0, largura, largura], y=[0, comprimento, comprimento, 0], z=[0, 0, 0, 0],
        i=[0, 0], j=[1, 2], k=[2, 3],
        opacity=0.1, color='#ffffff'
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Testada (m)', range=[0, largura + 5], backgroundcolor="#0a0a0a", gridcolor="#222"),
            yaxis=dict(title='Profundidade (m)', range=[0, comprimento + 5], backgroundcolor="#0a0a0a", gridcolor="#222"),
            zaxis=dict(title='Gabarito Máx (m)', range=[0, z_altura + 10], backgroundcolor="#0a0a0a", gridcolor="#222"),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=600
    )
    st.plotly_chart(fig, use_container_width=True)

# ABA 3: PARÂMETROS LEGAIS
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_tab_1, col_tab_2 = st.columns([2, 1])
    
    with col_tab_1:
        st.markdown("<h3>📋 TABELA DE ZONEAMENTO APLICADA</h3>", unsafe_allow_html=True)
        dados_tabela = {
            "DIRETRIZ URBANÍSTICA": ["Coeficiente de Aproveitamento (CA)", "Taxa de Ocupação Máxima (TO)", "Gabarito Máximo", "Recuo Frontal Obrigatório", "Recuo Lateral / Fundos"],
            "LIMITE LEGAL": [f"{regras['CA']}x a área do lote", f"{regras['TO']*100:.0f}%", f"{regras['Gabarito']} metros", f"{regras['Recuo_Frontal']} metros", f"{regras['Recuo_Lateral']} metros"]
        }
        df_regras = pd.DataFrame(dados_tabela)
        st.table(df_regras)
        
    with col_tab_2:
        st.markdown("<h3>📥 DOCUMENTAÇÃO OFICIAL</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #888; font-size: 14px;'>Acesse a legislação municipal na íntegra para validar casos de exceção ou outorga.</p>", unsafe_allow_html=True)
        
        # O arquivo precisa estar com esse nome exato no seu GitHub
        nome_arquivo = "Plano Diretor - Navegantes.pdf"
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, "rb") as file:
                st.download_button(label=f"⬇️ BAIXAR PLANO DIRETOR", data=file, file_name=nome_arquivo, mime="application/pdf")
        else:
            st.warning("O PDF original do Plano Diretor ainda não foi processado no banco de dados para download.")

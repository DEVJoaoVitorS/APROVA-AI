import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Aprova AI | Dashboard EVTL", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# INJEÇÃO DE CSS (ESTÉTICA CLEAN TECH / SAAS)
# ==========================================
estilo_clean = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Define a fonte padrão como Inter (ultra moderna e limpa) */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Fundo claro e moderno */
    .stApp {
        background-color: #F8FAFC !important; /* Cinza azulado bem sutil */
        color: #334155 !important; /* Texto grafite escuro */
    }
    
    /* Barra lateral branca e minimalista */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* Títulos em azul escuro corporativo */
    h1, h2, h3, h4 {
        color: #0F172A !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Customização das Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        border-bottom: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        color: #64748B;
        font-weight: 500;
        font-size: 14px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        color: #2563EB !important; /* Azul Tech */
        border-bottom: 2px solid #2563EB !important;
        font-weight: 600;
    }
    
    /* Inputs da barra lateral limpos */
    .stSelectbox div[data-baseweb="select"], .stNumberInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
        border-radius: 6px !important;
    }
    
    /* Cards de Métricas Estilo Dashboard Moderno */
    .metric-box {
        background-color: #FFFFFF;
        padding: 20px;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 12px;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
        margin-top: 5px;
    }
    
    /* Botões Limpos e Profissionais */
    .stDownloadButton>button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        width: 100%;
        transition: background-color 0.2s ease;
    }
    .stDownloadButton>button:hover {
        background-color: #1D4ED8 !important;
    }
    
    /* Tabelas limpas */
    [data-testid="stTable"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }
    
    hr { border-color: #E2E8F0 !important; }
</style>
"""
st.markdown(estilo_clean, unsafe_allow_html=True)

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
st.sidebar.markdown("<h3>📍 Localização</h3>", unsafe_allow_html=True)
cidade = st.sidebar.selectbox("Município", ["Navegantes - SC"])
zona = st.sidebar.selectbox("Zoneamento", list(zonas_mock.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("<h3>📐 Dimensões do Lote</h3>", unsafe_allow_html=True)
largura = st.sidebar.number_input("Testada / Largura (m)", min_value=5.0, value=12.0, step=0.5)
comprimento = st.sidebar.number_input("Profundidade / Comprimento (m)", min_value=10.0, value=25.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.markdown("<h3>💰 Premissas Comerciais</h3>", unsafe_allow_html=True)
tamanho_medio_apt = st.sidebar.number_input("Tamanho Médio da Unidade (m²)", min_value=20.0, value=65.0, step=1.0)
preco_venda_m2 = st.sidebar.number_input("Preço de Venda Esperado (R$/m²)", min_value=1000.0, value=8500.0, step=500.0)

# ==========================================
# CÁLCULOS MATEMÁTICOS
# ==========================================
regras = zonas_mock[zona]
area_terreno = largura * comprimento
area_max_computavel = area_terreno * regras["CA"]
area_projecao_maxima = area_terreno * regras["TO"]
area_ocupada_terreo = area_terreno * regras["TO"]
area_livre_terreo = area_terreno - area_ocupada_terreo

unidades_estimadas = int(area_max_computavel / tamanho_medio_apt)
vgv_estimado = area_max_computavel * preco_venda_m2

# ==========================================
# CABEÇALHO DO DASHBOARD
# ==========================================
st.markdown("<h1 style='font-size: 2.2rem; margin-bottom: 0; color: #0F172A;'>Aprova AI <span style='color: #2563EB; font-weight: 400;'>EVTL</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 14px; color: #64748B; margin-top: -5px;'>Plataforma Inteligente de Viabilidade Técnica e Legal</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# ESTRUTURA EM ABAS (ESTILO CLEAN TECH)
# ==========================================
tab1, tab2, tab3 = st.tabs(["📊 Resumo Executivo", "🏗️ Projeção Volumétrica 3D", "⚖️ Diretrizes e Leis"])

# ------------------------------------------
# ABA 1: RESUMO EXECUTIVO
# ------------------------------------------
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Linha de Indicadores rápidos
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>Área Total do Lote</div><div class='metric-value'>{area_terreno:,.0f} m²</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>Potencial de Construção</div><div class='metric-value'>{area_max_computavel:,.0f} m²</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>Capacidade de Unidades</div><div class='metric-value'>{unidades_estimadas} aptos</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>VGV Estimado Potencial</div><div class='metric-value'>R$ {vgv_estimado:,.0f}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Divisão para tabelas e novos gráficos analíticos
    col_analise_1, col_analise_2 = st.columns([1.2, 1])
    
    with col_analise_1:
        st.markdown("<h3>🎯 Análise de Aproveitamento Inteligente</h3>", unsafe_allow_html=True)
        st.markdown(f"O lote na zona **{zona}** possui um Coeficiente de Aproveitamento de **{regras['CA']}x**. Isso significa que você pode construir até {regras['CA']} vezes a área do terreno verticalmente, desde que respeite os recuos obrigatórios e a altura máxima.")
        
        # Alerta amigável estilo SaaS moderno
        st.info(f"💡 **Dica de Projeto:** A sua área de projeção máxima no solo é de **{area_ocupada_terreo:,.0f} m²**. Tente otimizar a modulação estrutural da garagem para ocupar o máximo dessa projeção permitida na base.")

    with col_analise_2:
        st.markdown("<h3>📊 Ocupação do Solo (Térreo)</h3>", unsafe_allow_html=True)
        
        # Gráfico Donut de Ocupação do Terreno
        fig_donut = go.Figure(data=[go.Pie(
            labels=['Área Ocupável (TO)', 'Área Livre / Permeável'],
            values=[area_ocupada_terreo, area_livre_terreo],
            hole=.5,
            marker_colors=['#2563EB', '#E2E8F0'] # Azul tech e cinza claro
        )])
        fig_donut.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            height=220,
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_donut, use_container_width=True)

# ------------------------------------------
# ABA 2: MODELAGEM VOLUMÉTRICA 3D
# ------------------------------------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3>Envelope Máximo Edificável</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 14px;'>O bloco azul representa o volume tridimensional máximo que a sua edificação pode ocupar, respeitando os recuos e gabarito.</p>", unsafe_allow_html=True)
    
    x_inicio = regras["Recuo_Lateral"]
    x_fim = largura - regras["Recuo_Lateral"]
    y_inicio = regras["Recuo_Frontal"]
    y_fim = comprimento - regras["Recuo_Frontal"]
    z_altura = regras["Gabarito"]

    # Modelo 3D com paleta clara (Estilo CAD)
    fig_3d = go.Figure(data=[
        go.Mesh3d(
            x=[x_inicio, x_inicio, x_fim, x_fim, x_inicio, x_inicio, x_fim, x_fim],
            y=[y_inicio, y_fim, y_fim, y_inicio, y_inicio, y_fim, y_fim, y_inicio],
            z=[0, 0, 0, 0, z_altura, z_altura, z_altura, z_altura],
            i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            opacity=0.5, color='#3B82F6', flatshading=True # Azul translúcido moderno
        )
    ])
    
    # Base do terreno branca/cinza
    fig_3d.add_trace(go.Mesh3d(
        x=[0, 0, largura, largura], y=[0, comprimento, comprimento, 0], z=[0, 0, 0, 0],
        i=[0, 0], j=[1, 2], k=[2, 3],
        opacity=0.15, color='#0F172A'
    ))

    fig_3d.update_layout(
        scene=dict(
            xaxis=dict(title='Largura (m)', range=[0, largura + 5], backgroundcolor="#F1F5F9", gridcolor="#E2E8F0"),
            yaxis=dict(title='Profundidade (m)', range=[0, comprimento + 5], backgroundcolor="#F1F5F9", gridcolor="#E2E8F0"),
            zaxis=dict(title='Altura (m)', range=[0, z_altura + 10], backgroundcolor="#F1F5F9", gridcolor="#E2E8F0"),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=550
    )
    st.plotly_chart(fig_3d, use_container_width=True)

# ------------------------------------------
# ABA 3: DIRETRIZES E LEIS
# ------------------------------------------
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    col_tab_1, col_tab_2 = st.columns([1.8, 1])
    
    with col_tab_1:
        st.markdown("<h3>📋 Parâmetros Urbanísticos Oficiais</h3>", unsafe_allow_html=True)
        dados_tabela = {
            "DIRETRIZ URBANÍSTICA": ["Coeficiente de Aproveitamento (CA)", "Taxa de Ocupação Máxima (TO)", "Gabarito Máximo de Altura", "Recuo Frontal Obrigatório", "Recuo Lateral e Fundos Mínimo"],
            "LIMITE LEGAL APLICADO": [f"{regras['CA']}x a área nominal", f"{regras['TO']*100:.0f}% do lote", f"{regras['Gabarito']} metros", f"{regras['Recuo_Frontal']} metros", f"{regras['Recuo_Lateral']} metros"]
        }
        df_regras = pd.DataFrame(dados_tabela)
        st.table(df_regras)
        
    with col_tab_2:
        st.markdown("<h3>📥 Legislação para Download</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 14px;'>Clique no botão abaixo para baixar a versão original digitalizada do Plano Diretor de Navegantes.</p>", unsafe_allow_html=True)
        
        nome_arquivo = "Plano Diretor - Navegantes.pdf"
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, "rb") as file:
                st.download_button(label="⬇️ BAIXAR PLANO DIRETOR (PDF)", data=file, file_name=nome_arquivo, mime="application/pdf")
        else:
            st.warning("O documento 'Plano Diretor - Navegantes.pdf' não foi encontrado na raiz do seu GitHub.")

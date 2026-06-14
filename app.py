import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from fpdf import FPDF

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(page_title="Aprova AI | Dashboard", layout="wide")

# ==========================================
# 2. INJEÇÃO DE CSS (ESTÉTICA SQUAD-EASY: CLEAN, CORPORATE, GREEN)
# ==========================================
st.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #1E293B;
    }
    
    /* Fundo limpo corporativo */
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    /* Sidebar Profissional */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    h1, h2, h3 {
        color: #0F172A !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }

    /* Cards e Elementos - Estilo SquadEasy (Arredondado + Sombra leve) */
    .metric-card {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.05);
    }

    .metric-label { font-size: 12px; color: #64748B; font-weight: 600; text-transform: uppercase; }
    .metric-value { font-size: 24px; color: #0F172A; font-weight: 700; margin-top: 8px; }

    /* Botões em Verde Corporativo */
    .stButton>button, .stDownloadButton>button {
        background-color: #22C55E !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 10px 20px !important;
    }
    .stButton>button:hover {
        background-color: #16A34A !important;
    }

    /* Tabs limpas */
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: #64748B;
    }
    .stTabs [aria-selected="true"] {
        color: #22C55E !important;
    }
    
    /* Alertas */
    .success-box { background: #DCFCE7; border-left: 4px solid #22C55E; padding: 15px; border-radius: 4px; color: #166534; }
    .error-box { background: #FEE2E2; border-left: 4px solid #EF4444; padding: 15px; border-radius: 4px; color: #991B1B; }
</style>
""")

# ==========================================
# 3. DADOS E LÓGICA (MANTIDA)
# ==========================================
zonas_mock = {
    "ZR1 (Residencial)": {"CA": 2.0, "TO": 0.60, "Gabarito": 15, "Recuo_Frontal": 4.0, "Recuo_Lateral": 1.5, "Lote_Minimo": 300, "Testada_Minima": 12.0},
    "ZCC (Comercial)": {"CA": 4.0, "TO": 0.80, "Gabarito": 30, "Recuo_Frontal": 3.0, "Recuo_Lateral": 0.0, "Lote_Minimo": 250, "Testada_Minima": 10.0}
}

# ... (Inputs laterais)
cidade = st.sidebar.selectbox("Cidade", ["Navegantes - SC"])
zona = st.sidebar.selectbox("Zona", list(zonas_mock.keys()))
largura = st.sidebar.number_input("Testada (m)", value=12.0)
comprimento = st.sidebar.number_input("Profundidade (m)", value=25.0)
tamanho_medio_apt = st.sidebar.number_input("Área por apto (m²)", value=65.0)
preco_venda_m2 = st.sidebar.number_input("VGV (R$/m²)", value=8500.0)

regras = zonas_mock[zona]
area_terreno = largura * comprimento
erros = []
if area_terreno < regras["Lote_Minimo"]: erros.append("Área do lote insuficiente.")
if largura < regras["Testada_Minima"]: erros.append("Testada mínima não atingida.")
aprovado = len(erros) == 0

# ==========================================
# 4. INTERFACE LIMPA
# ==========================================
st.title("Aprova AI")
st.subheader("Consultoria de Viabilidade Técnica e Legal")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["RESUMO", "VOLUMETRIA", "NORMAS"])

with tab1:
    if aprovado:
        st.markdown("<div class='success-box'>✅ Parâmetros em conformidade com o Plano Diretor.</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-label'>Área Total</div><div class='metric-value'>{area_terreno:,.0f} m²</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-label'>Potencial (CA)</div><div class='metric-value'>{(area_terreno*regras['CA']):,.0f} m²</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-label'>Unidades</div><div class='metric-value'>{int((area_terreno*regras['CA'])/tamanho_medio_apt)}</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='metric-card'><div class='metric-label'>VGV Est.</div><div class='metric-value'>R$ {(area_terreno*regras['CA']*preco_venda_m2)/1000000:.1f}M</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='error-box'>⚠️ Verifique as pendências: {', '.join(erros)}</div>", unsafe_allow_html=True)

with tab2:
    if aprovado:
        fig = go.Figure(data=[go.Mesh3d(x=[0,0,largura,largura,0,0,largura,largura], y=[0,comprimento,comprimento,0,0,comprimento,comprimento,0], z=[0,0,0,0,regras['Gabarito'],regras['Gabarito'],regras['Gabarito'],regras['Gabarito']], color='#22C55E', opacity=0.5)])
        fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Ajuste as dimensões para liberar a visualização 3D.")

with tab3:
    st.table(pd.DataFrame({"Norma": ["Recuo Frontal", "Recuo Lateral", "TO Máx", "CA"], "Valor": [f"{regras['Recuo_Frontal']}m", f"{regras['Recuo_Lateral']}m", f"{regras['TO']*100}%", regras['CA']]}))

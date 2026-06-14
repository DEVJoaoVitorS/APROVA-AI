import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from fpdf import FPDF

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(page_title="Aprova AI | EVTL", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 2. INJEÇÃO DE CSS (ESTÉTICA STAR ATLAS / HIGH-TECH)
# ==========================================
# Aqui usamos st.html para forçar a importação da fonte Orbitron (muito usada em Sci-Fi/Games)
st.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    /* Fundo Espacial / Dark Mode Absoluto */
    .stApp {
        background-color: #050505 !important;
        color: #E2E8F0 !important;
        background-image: radial-gradient(circle at 50% 0%, #111827 0%, #050505 70%);
    }
    
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #1E293B !important;
    }
    
    /* Fontes Futuristas para Títulos */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #FFFFFF !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
    }
    
    .stNumberInput label, .stSelectbox label {
        color: #94A3B8 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 11px !important;
        letter-spacing: 1.5px !important;
    }
    
    /* CAIXAS HIGH-TECH (HUD ESTILO STAR ATLAS) */
    .metric-box {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(10px);
        padding: 20px;
        border: 1px solid #1E293B;
        border-radius: 4px; /* Bordas cortadas/retas mais tecnológicas */
        border-left: 2px solid #00F0FF; /* Neon Cyan */
        margin-bottom: 16px;
        transition: all 0.3s ease-in-out;
    }
    
    /* Efeito Glowing (Brilho Neon) no Hover */
    .metric-box:hover {
        transform: translateY(-5px);
        background: rgba(30, 41, 59, 0.8);
        border-left: 4px solid #00F0FF;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    }
    
    .metric-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 10px;
        color: #00F0FF;
        letter-spacing: 2px;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 5px;
    }
    
    /* BOTÕES COM EFEITO NEON */
    .stButton>button, .stDownloadButton>button {
        background: transparent !important;
        color: #00F0FF !important;
        border: 1px solid #00F0FF !important;
        border-radius: 2px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 12px !important;
        letter-spacing: 2px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: inset 0 0 10px rgba(0, 240, 255, 0.1);
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: #00F0FF !important;
        color: #000000 !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.5) !important;
    }
    
    /* ABAS CYBERPUNK */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid #1E293B;
    }
    .stTabs [data-baseweb="tab"] {
        color: #64748B;
        font-family: 'Orbitron', sans-serif;
        font-size: 11px;
        letter-spacing: 1.5px;
    }
    .stTabs [aria-selected="true"] {
        color: #00F0FF !important;
        border-bottom: 2px solid #00F0FF !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    }
    
    /* ALERTAS CUSTOMIZADOS */
    .alerta-aprovado {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #10B981;
        padding: 15px;
        box-shadow: inset 0 0 15px rgba(16, 185, 129, 0.2);
    }
    .alerta-reprovado {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #EF4444;
        padding: 15px;
        box-shadow: inset 0 0 15px rgba(239, 68, 68, 0.2);
        animation: pulseError 2s infinite;
    }
    @keyframes pulseError {
        0% { box-shadow: inset 0 0 15px rgba(239, 68, 68, 0.2); }
        50% { box-shadow: inset 0 0 25px rgba(239, 68, 68, 0.5); }
        100% { box-shadow: inset 0 0 15px rgba(239, 68, 68, 0.2); }
    }
    .alerta-titulo { font-family: 'Orbitron', sans-serif; font-size: 12px; margin-bottom: 5px; }
    .aprovado-txt { color: #10B981; }
    .reprovado-txt { color: #EF4444; }
</style>
""")

# ==========================================
# 3. DADOS DE ZONEAMENTO E REGRAS DE VALIDAÇÃO
# ==========================================
zonas_mock = {
    "ZR1 (Zona Residencial 1)": {
        "CA": 2.0, "TO": 0.60, "Gabarito": 15, "Recuo_Frontal": 4.0, "Recuo_Lateral": 1.5,
        "Lote_Minimo": 300, "Testada_Minima": 12.0
    },
    "ZCC (Zona Comercial Central)": {
        "CA": 4.0, "TO": 0.80, "Gabarito": 30, "Recuo_Frontal": 3.0, "Recuo_Lateral": 0.0,
        "Lote_Minimo": 250, "Testada_Minima": 10.0
    }
}

# ==========================================
# 4. INTERFACE LATERAL (INPUTS)
# ==========================================
st.sidebar.markdown("<h3>LOCALIZAÇÃO DO ATIVO</h3>", unsafe_allow_html=True)
cidade = st.sidebar.selectbox("MUNICÍPIO", ["Navegantes - SC"])
zona = st.sidebar.selectbox("ZONEAMENTO", list(zonas_mock.keys()))

st.sidebar.markdown("<br><h3>GEOMETRIA BASE</h3>", unsafe_allow_html=True)
largura = st.sidebar.number_input("TESTADA (m)", min_value=1.0, value=12.0, step=0.5)
comprimento = st.sidebar.number_input("PROFUNDIDADE (m)", min_value=1.0, value=25.0, step=0.5)

st.sidebar.markdown("<br><h3>PARÂMETROS COMERCIAIS</h3>", unsafe_allow_html=True)
tamanho_medio_apt = st.sidebar.number_input("ÁREA UNIDADE (m²)", min_value=20.0, value=65.0, step=1.0)
preco_venda_m2 = st.sidebar.number_input("VGV BASE (R$/m²)", min_value=1000.0, value=8500.0, step=500.0)

# ==========================================
# 5. MOTOR DE VERIFICAÇÃO E CÁLCULO
# ==========================================
regras = zonas_mock[zona]
area_terreno = largura * comprimento

erros_normativos = []
if area_terreno < regras["Lote_Minimo"]:
    erros_normativos.append(f"INCOMPATÍVEL: Área do lote ({area_terreno:.0f} m²) inferior ao Mínimo Legal ({regras['Lote_Minimo']} m²).")
if largura < regras["Testada_Minima"]:
    erros_normativos.append(f"INCOMPATÍVEL: Testada ({largura:.1f} m) inferior ao Mínimo Legal ({regras['Testada_Minima']} m).")

aprovado = len(erros_normativos) == 0

if aprovado:
    area_max_computavel = area_terreno * regras["CA"]
    area_ocupada_terreo = area_terreno * regras["TO"]
    area_livre_terreo = area_terreno - area_ocupada_terreo
    unidades_estimadas = int(area_max_computavel / tamanho_medio_apt)
    vgv_estimado = area_max_computavel * preco_venda_m2
else:
    area_max_computavel = area_ocupada_terreo = area_livre_terreo = unidades_estimadas = vgv_estimado = 0

# ==========================================
# 6. GERAÇÃO DE PDF
# ==========================================
def gerar_pdf_evtl():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "ESTUDO DE VIABILIDADE TECNICA E LEGAL (EVTL)", ln=True, align="C")
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "Sistema de Inteligencia Parametrica", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "1. DADOS", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, f"Municipio: {cidade} | Zona: {zona}", ln=True)
    pdf.cell(0, 6, f"Area Total: {area_terreno:.2f} m2", ln=True)
    pdf.ln(5)
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 7. INTERFACE PRINCIPAL
# ==========================================
st.markdown("<h1>APROVA AI <span style='color: #00F0FF; font-weight: 400;'>// EVTL CORE</span></h1>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["[ RESUMO EXECUTIVO ]", "[ MODELAGEM 3D ]", "[ PROTOCOLOS LEGAIS ]"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if aprovado:
        st.markdown("""
        <div class='alerta-aprovado'>
            <div class='alerta-titulo aprovado-txt'>SISTEMA: PARÂMETROS APROVADOS</div>
            <div style='color: #E2E8F0; font-size: 14px;'>A conformidade legal foi atestada pelos protocolos urbanísticos ativos.</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>TERRENO TOTAL</div><div class='metric-value'>{area_terreno:,.0f} m²</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>POTENCIAL CONSTRUTIVO</div><div class='metric-value'>{area_max_computavel:,.0f} m²</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>CAPACIDADE PROJETADA</div><div class='metric-value'>{unidades_estimadas} UDS</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>ESTIMATIVA VGV</div><div class='metric-value'>R$ {vgv_estimado:,.0f}</div></div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        col_graf_1, col_graf_2 = st.columns([1, 1])
        with col_graf_1:
            st.markdown("<h3>DISTRIBUIÇÃO DE SOLO</h3>", unsafe_allow_html=True)
            fig_donut = go.Figure(data=[go.Pie(
                labels=['PROJEÇÃO MÁX', 'ÁREA PERMEÁVEL'],
                values=[area_ocupada_terreo, area_livre_terreo], hole=.7,
                marker_colors=['#00F0FF', '#1E293B']
            )])
            fig_donut.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=250, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#FFFFFF', family="Rajdhani"))
            st.plotly_chart(fig_donut, use_container_width=True)
            
        with col_graf_2:
            st.markdown("<h3>EXPORTAÇÃO DE LAUDO</h3>", unsafe_allow_html=True)
            pdf_bytes = gerar_pdf_evtl()
            st.download_button("INICIAR DOWNLOAD DO RELATÓRIO", data=pdf_bytes, file_name=f"EVTL_{cidade.split()[0]}.pdf", mime="application/pdf")

    else:
        html_erros = "".join([f"<li style='color: #E2E8F0; font-size: 14px;'>{erro}</li>" for erro in erros_normativos])
        st.markdown(f"""
        <div class='alerta-reprovado'>
            <div class='alerta-titulo reprovado-txt'>ALERTA: VIOLAÇÃO DE PARÂMETROS LEGAIS</div>
            <ul style='margin-top: 10px;'>{html_erros}</ul>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    if aprovado:
        st.markdown("<h3>RENDERIZAÇÃO DO ENVELOPE</h3>", unsafe_allow_html=True)
        
        x_inicio = regras["Recuo_Lateral"]
        x_fim = largura - regras["Recuo_Lateral"]
        y_inicio = regras["Recuo_Frontal"]
        y_fim = comprimento - regras["Recuo_Frontal"]
        z_altura = regras["Gabarito"]

        fig_3d = go.Figure(data=[
            go.Mesh3d(
                x=[x_inicio, x_inicio, x_fim, x_fim, x_inicio, x_inicio, x_fim, x_fim],
                y=[y_inicio, y_fim, y_fim, y_inicio, y_inicio, y_fim, y_fim, y_inicio],
                z=[0, 0, 0, 0, z_altura, z_altura, z_altura, z_altura],
                i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2], j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3], k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                opacity=0.3, color='#00F0FF', flatshading=True # Bloco holográfico
            )
        ])
        fig_3d.add_trace(go.Mesh3d(
            x=[0, 0, largura, largura], y=[0, comprimento, comprimento, 0], z=[0, 0, 0, 0],
            i=[0, 0], j=[1, 2], k=[2, 3], opacity=0.1, color='#FFFFFF'
        ))

        fig_3d.update_layout(
            scene=dict(
                xaxis=dict(title='X', backgroundcolor="#050505", gridcolor="#1E293B", color="#00F0FF"),
                yaxis=dict(title='Y', backgroundcolor="#050505", gridcolor="#1E293B", color="#00F0FF"),
                zaxis=dict(title='Z', backgroundcolor="#050505", gridcolor="#1E293B", color="#00F0FF"),
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor='rgba(0,0,0,0)', height=550, font=dict(family="Orbitron")
        )
        st.plotly_chart(fig_3d, use_container_width=True)
    else:
        st.error("RENDERIZAÇÃO BLOQUEADA DEVIDO A INFRAÇÕES TÉCNICAS.")

with tab3:
    st.markdown("<br><h3>MATRIZ LEGISLATIVA</h3>", unsafe_allow_html=True)
    dados_tabela = {
        "DIRETRIZ": ["Área Min", "Testada", "C.A.", "T.O.", "Gabarito Máx"],
        "VALOR LIMITE": [f"{regras['Lote_Minimo']} m²", f"{regras['Testada_Minima']} m", f"{regras['CA']}x", f"{regras['TO']*100:.0f}%", f"{regras['Gabarito']} m"]
    }
    st.table(pd.DataFrame(dados_tabela))

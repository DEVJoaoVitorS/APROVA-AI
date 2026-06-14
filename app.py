import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64
from fpdf import FPDF

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(page_title="Aprova AI | Dashboard EVTL", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 2. INJEÇÃO DE CSS (ANIMAÇÕES E FIX DE CORES)
# ==========================================
estilo_interativo = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp {
        background-color: #F8FAFC !important;
        color: #334155 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* CORREÇÃO DOS TÍTULOS LATERAIS INVISÍVEIS */
    .stNumberInput label, .stSelectbox label {
        color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        letter-spacing: 0.2px !important;
    }
    
    /* ANIMAÇÃO DE ENTRADA (FADE IN UP) */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* APLICAÇÃO DAS ANIMAÇÕES E EFEITOS HOVER */
    .metric-box, .status-box, .stPlotlyChart {
        animation: fadeInUp 0.6s ease-out forwards;
        background-color: #FFFFFF;
        padding: 24px;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* EFEITO AO PASSAR O MOUSE (INTERATIVIDADE) */
    .metric-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.08);
        border-color: #3B82F6;
    }
    
    .metric-title {
        font-size: 12px;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #0F172A;
        margin-top: 6px;
    }
    
    /* DESIGN DOS BOTÕES (SaaS Moderno) */
    .stButton>button, .stDownloadButton>button {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        width: 100%;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #3B82F6 !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        transform: scale(1.02);
    }
    
    /* CUSTOMIZAÇÃO DAS ABAS - SEM EMOJIS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        color: #64748B;
        font-weight: 600;
        font-size: 13px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        padding: 15px 5px;
    }
    .stTabs [aria-selected="true"] {
        color: #0F172A !important;
        border-bottom: 2px solid #0F172A !important;
    }
</style>
"""
st.markdown(estilo_interativo, unsafe_allow_html=True)

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
st.sidebar.markdown("<h3 style='color: #0F172A; font-size: 16px;'>LOCALIZAÇÃO E ZONAS</h3>", unsafe_allow_html=True)
cidade = st.sidebar.selectbox("MUNICÍPIO", ["Navegantes - SC"])
zona = st.sidebar.selectbox("ZONEAMENTO APLICÁVEL", list(zonas_mock.keys()))

st.sidebar.markdown("<br><h3 style='color: #0F172A; font-size: 16px;'>GEOMETRIA DO LOTE</h3>", unsafe_allow_html=True)
largura = st.sidebar.number_input("TESTADA PRINCIPAL (m)", min_value=1.0, value=12.0, step=0.5)
comprimento = st.sidebar.number_input("PROFUNDIDADE (m)", min_value=1.0, value=25.0, step=0.5)

st.sidebar.markdown("<br><h3 style='color: #0F172A; font-size: 16px;'>VARIÁVEIS COMERCIAIS</h3>", unsafe_allow_html=True)
tamanho_medio_apt = st.sidebar.number_input("ÁREA PRIVATIVA MÉDIA (m²)", min_value=20.0, value=65.0, step=1.0)
preco_venda_m2 = st.sidebar.number_input("PREÇO DE VENDA (R$/m²)", min_value=1000.0, value=8500.0, step=500.0)

# ==========================================
# 5. MOTOR DE VERIFICAÇÃO E CÁLCULO
# ==========================================
regras = zonas_mock[zona]
area_terreno = largura * comprimento

# Motor de Validação Normativa (Gatilho de Reprovação)
erros_normativos = []
if area_terreno < regras["Lote_Minimo"]:
    erros_normativos.append(f"Área do lote ({area_terreno:.0f} m²) é inferior ao mínimo legal da {zona[:3]} ({regras['Lote_Minimo']} m²).")
if largura < regras["Testada_Minima"]:
    erros_normativos.append(f"Testada do lote ({largura:.1f} m) é inferior à mínima legal da {zona[:3]} ({regras['Testada_Minima']} m).")

aprovado = len(erros_normativos) == 0

# Cálculos se aprovado
if aprovado:
    area_max_computavel = area_terreno * regras["CA"]
    area_ocupada_terreo = area_terreno * regras["TO"]
    area_livre_terreo = area_terreno - area_ocupada_terreo
    unidades_estimadas = int(area_max_computavel / tamanho_medio_apt)
    vgv_estimado = area_max_computavel * preco_venda_m2
else:
    area_max_computavel = area_ocupada_terreo = area_livre_terreo = unidades_estimadas = vgv_estimado = 0

# ==========================================
# 6. GERAÇÃO AUTÔNOMA DE RELATÓRIO (PDF)
# ==========================================
def gerar_pdf_evtl():
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "ESTUDO DE VIABILIDADE TECNICA E LEGAL (EVTL)", ln=True, align="C")
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "Gerado pelo Sistema Aprova AI", ln=True, align="C")
    pdf.ln(10)
    
    # Corpo do Relatório
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "1. DADOS DA LOCALIZACAO", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, f"Municipio: {cidade}", ln=True)
    pdf.cell(0, 6, f"Zoneamento: {zona}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "2. PARAMETROS GEOMETRICOS DO LOTE", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, f"Dimensoes: {largura}m x {comprimento}m", ln=True)
    pdf.cell(0, 6, f"Area Total: {area_terreno:.2f} m2", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "3. LIMITES CONSTRUTIVOS APROVADOS", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, f"Coeficiente de Aproveitamento (CA): {regras['CA']}", ln=True)
    pdf.cell(0, 6, f"Potencial Maximo Computavel: {area_max_computavel:.2f} m2", ln=True)
    pdf.cell(0, 6, f"Taxa de Ocupacao Terea (TO): {regras['TO']*100}%", ln=True)
    pdf.cell(0, 6, f"Gabarito Maximo de Altura: {regras['Gabarito']} metros", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "4. ESTIMATIVA COMERCIAL", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, f"Capacidade Estimada: {unidades_estimadas} unidades", ln=True)
    pdf.cell(0, 6, f"Valor Geral de Vendas (VGV) Projetado: R$ {vgv_estimado:,.2f}", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 7. INTERFACE PRINCIPAL
# ==========================================
st.markdown("<h1 style='font-size: 2.2rem; color: #0F172A; margin-bottom: 0;'>APROVA AI <span style='font-weight: 300; color: #64748B;'>| PLATAFORMA EVTL</span></h1>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["RESUMO EXECUTIVO", "MODELAGEM VOLUMÉTRICA", "BASE NORMATIVA"])

# ------------------------------------------
# ABA 1: RESUMO EXECUTIVO (COM LÓGICA DE VALIDAÇÃO)
# ------------------------------------------
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bloco de Status da Aprovação
    if aprovado:
        st.success("✔️ VIABILIDADE PRÉ-APROVADA: Os parâmetros do lote atendem às restrições mínimas do Plano Diretor.")
        
        # Métricas apenas se aprovado
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>Área do Terreno</div><div class='metric-value'>{area_terreno:,.0f} m²</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>Potencial Máx (CA)</div><div class='metric-value'>{area_max_computavel:,.0f} m²</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>Capacidade</div><div class='metric-value'>{unidades_estimadas} uds</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>VGV Estimado</div><div class='metric-value'>R$ {vgv_estimado:,.0f}</div></div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos Analíticos
        col_graf_1, col_graf_2 = st.columns([1, 1])
        with col_graf_1:
            st.markdown("<h3 style='font-size: 16px; color: #0F172A;'>DISTRIBUIÇÃO DE SOLO</h3>", unsafe_allow_html=True)
            fig_donut = go.Figure(data=[go.Pie(
                labels=['Área de Projeção Permitida', 'Área Permeável Obrigatória'],
                values=[area_ocupada_terreo, area_livre_terreo],
                hole=.6,
                marker_colors=['#0F172A', '#E2E8F0']
            )])
            fig_donut.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=250, paper_bgcolor='rgba(0,0,0,0)', showlegend=True)
            st.plotly_chart(fig_donut, use_container_width=True)
            
        with col_graf_2:
            st.markdown("<h3 style='font-size: 16px; color: #0F172A;'>AÇÃO REQUERIDA</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #64748B; font-size: 14px;'>A conformidade legal foi estabelecida. Gere o laudo técnico automático para anexar à sua documentação de projeto.</p>", unsafe_allow_html=True)
            
            # Botão de Gerar PDF Autônomo
            pdf_bytes = gerar_pdf_evtl()
            st.download_button(
                label="GERAR RELATÓRIO EVTL (PDF)",
                data=pdf_bytes,
                file_name=f"EVTL_Aprova_AI_{cidade.split()[0]}.pdf",
                mime="application/pdf"
            )

    else:
        # Se Reprovado, mostra alertas e esconde os dados de viabilidade
        st.error("❌ VIABILIDADE REPROVADA: Inconformidade com a legislação urbanística.")
        st.markdown("<div class='status-box' style='border-left: 4px solid #EF4444;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #EF4444; font-size: 16px;'>MOTIVO DA REPROVAÇÃO TÉCNICA:</h3>", unsafe_allow_html=True)
        for erro in erros_normativos:
            st.markdown(f"<p style='font-weight: 600;'>• {erro}</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 14px; mt-4;'>Modifique os parâmetros do lote no menu lateral para realizar uma nova simulação ou solicite o enquadramento de exceção via outorga onerosa na prefeitura.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------
# ABA 2: MODELAGEM VOLUMÉTRICA
# ------------------------------------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    if aprovado:
        st.markdown("<h3 style='font-size: 16px; color: #0F172A;'>ENVELOPE MÁXIMO EDIFICÁVEL</h3>", unsafe_allow_html=True)
        
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
                i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                opacity=0.8, color='#0F172A', flatshading=True
            )
        ])
        
        fig_3d.add_trace(go.Mesh3d(
            x=[0, 0, largura, largura], y=[0, comprimento, comprimento, 0], z=[0, 0, 0, 0],
            i=[0, 0], j=[1, 2], k=[2, 3], opacity=0.1, color='#64748B'
        ))

        fig_3d.update_layout(
            scene=dict(
                xaxis=dict(title='Testada (m)', backgroundcolor="#F8FAFC", gridcolor="#E2E8F0"),
                yaxis=dict(title='Profundidade (m)', backgroundcolor="#F8FAFC", gridcolor="#E2E8F0"),
                zaxis=dict(title='Altura Máx (m)', backgroundcolor="#F8FAFC", gridcolor="#E2E8F0"),
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='rgba(0,0,0,0)', height=550
        )
        st.plotly_chart(fig_3d, use_container_width=True)
    else:
        st.warning("O lote encontra-se em inconformidade normativa. A modelagem espacial foi bloqueada até a regularização da geometria base.")

# ------------------------------------------
# ABA 3: BASE NORMATIVA
# ------------------------------------------
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    col_tab_1, col_tab_2 = st.columns([1.8, 1])
    
    with col_tab_1:
        st.markdown("<h3 style='font-size: 16px; color: #0F172A;'>DIRETRIZES LEGAIS APLICADAS</h3>", unsafe_allow_html=True)
        dados_tabela = {
            "DISPOSITIVO LEGAL": ["Área Mínima de Loteamento", "Testada Mínima Exigida", "Coeficiente de Aproveitamento (CA)", "Taxa de Ocupação Máxima (TO)", "Gabarito de Altura", "Recuo Frontal", "Recuo Lateral e Fundos"],
            "RESTRIÇÃO": [f"{regras['Lote_Minimo']} m²", f"{regras['Testada_Minima']} metros", f"{regras['CA']}x a área nominal", f"{regras['TO']*100:.0f}%", f"{regras['Gabarito']} metros", f"{regras['Recuo_Frontal']} metros", f"{regras['Recuo_Lateral']} metros"]
        }
        st.table(pd.DataFrame(dados_tabela))
        
    with col_tab_2:
        st.markdown("<h3 style='font-size: 16px; color: #0F172A;'>CÓDIGO DE ORIGEM</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 14px;'>Faça o download do documento oficial fornecido pela prefeitura para consulta de artigos específicos.</p>", unsafe_allow_html=True)
        
        nome_arquivo = "Plano Diretor - Navegantes.pdf"
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, "rb") as file:
                st.download_button(label="DOWNLOAD ARQUIVO MATRIZ", data=file, file_name=nome_arquivo, mime="application/pdf")
        else:
            st.warning(f"O documento base {nome_arquivo} está ausente no servidor.")

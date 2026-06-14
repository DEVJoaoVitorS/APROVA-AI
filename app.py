import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from fpdf import FPDF

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(page_title="Aprova AI | Dashboard EVTL", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 2. INJEÇÃO DE CSS (DESIGN JOVEM, FONTE OUTFIT E ANIMAÇÕES EXAGERADAS)
# ==========================================
estilo_interativo = """
<style>
    /* Fonte Outfit: Jovem, geométrica e muito moderna */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    .stApp {
        background-color: #F4F7FB !important; /* Fundo levemente mais claro/frio */
        color: #1E293B !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* TITULOS E LABELS */
    h1, h2, h3, h4 {
        color: #0F172A !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }
    .stNumberInput label, .stSelectbox label {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }
    
    /* CAIXAS DE ALERTAS CUSTOMIZADAS (SEM EMOJIS) */
    .alerta-aprovado {
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
        padding: 16px 24px;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    .alerta-reprovado {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 16px 24px;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    .alerta-titulo {
        font-weight: 800;
        font-size: 15px;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .alerta-aprovado .alerta-titulo { color: #047857; }
    .alerta-reprovado .alerta-titulo { color: #B91C1C; }
    .alerta-texto { font-size: 14px; font-weight: 400; color: #334155; }
    
    /* ANIMAÇÃO DE ENTRADA */
    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* EFEITOS DE HOVER APRIMORADOS NAS CAIXAS */
    .metric-box {
        animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        background-color: #FFFFFF;
        padding: 24px;
        border: 1px solid #E2E8F0;
        border-radius: 16px; /* Mais arredondado = Mais jovem */
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 16px;
        /* Transição elástica estilo "bouncy" */
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    /* INTERATIVIDADE MOUSE OVER - O EFEITO DE SALTO */
    .metric-box:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
        border-color: #3B82F6;
    }
    
    .metric-title {
        font-size: 11px;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 800;
        color: #0F172A;
        margin-top: 6px;
        letter-spacing: -1px;
    }
    
    /* DESIGN DOS BOTÕES DE AÇÃO */
    .stButton>button, .stDownloadButton>button {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 0.5px !important;
        padding: 14px 24px !important;
        width: 100%;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #2563EB !important;
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3) !important;
    }
    
    /* ABAS MINIMALISTAS (SEM EMOJIS) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid #CBD5E1;
    }
    .stTabs [data-baseweb="tab"] {
        color: #64748B;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 15px 5px;
    }
    .stTabs [aria-selected="true"] {
        color: #2563EB !important; /* Azul tech vibrante ao selecionar */
        border-bottom: 3px solid #2563EB !important;
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
st.sidebar.markdown("<h3 style='color: #0F172A; font-size: 15px; margin-bottom: 0px;'>LOCALIZAÇÃO DO ATIVO</h3>", unsafe_allow_html=True)
cidade = st.sidebar.selectbox("MUNICÍPIO", ["Navegantes - SC"])
zona = st.sidebar.selectbox("ZONEAMENTO APLICÁVEL", list(zonas_mock.keys()))

st.sidebar.markdown("<br><h3 style='color: #0F172A; font-size: 15px; margin-bottom: 0px;'>GEOMETRIA DO LOTE</h3>", unsafe_allow_html=True)
largura = st.sidebar.number_input("TESTADA PRINCIPAL (m)", min_value=1.0, value=12.0, step=0.5)
comprimento = st.sidebar.number_input("PROFUNDIDADE (m)", min_value=1.0, value=25.0, step=0.5)

st.sidebar.markdown("<br><h3 style='color: #0F172A; font-size: 15px; margin-bottom: 0px;'>PREMISSAS COMERCIAIS</h3>", unsafe_allow_html=True)
tamanho_medio_apt = st.sidebar.number_input("ÁREA PRIVATIVA MÉDIA (m²)", min_value=20.0, value=65.0, step=1.0)
preco_venda_m2 = st.sidebar.number_input("PREÇO DE VENDA (R$/m²)", min_value=1000.0, value=8500.0, step=500.0)

# ==========================================
# 5. MOTOR DE VERIFICAÇÃO E CÁLCULO
# ==========================================
regras = zonas_mock[zona]
area_terreno = largura * comprimento

# Motor de Validação Normativa
erros_normativos = []
if area_terreno < regras["Lote_Minimo"]:
    erros_normativos.append(f"Área do lote ({area_terreno:.0f} m²) é inferior ao mínimo legal da {zona[:3]} ({regras['Lote_Minimo']} m²).")
if largura < regras["Testada_Minima"]:
    erros_normativos.append(f"Testada do lote ({largura:.1f} m) é inferior à mínima legal da {zona[:3]} ({regras['Testada_Minima']} m).")

aprovado = len(erros_normativos) == 0

# Cálculos Executivos
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
    pdf.cell(0, 6, f"Taxa de Ocupacao Terrea (TO): {regras['TO']*100}%", ln=True)
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
st.markdown("<h1 style='font-size: 2.5rem; color: #0F172A; margin-bottom: 0; font-weight: 800;'>APROVA AI <span style='font-weight: 300; color: #94A3B8;'>| PLATAFORMA EVTL</span></h1>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["RESUMO EXECUTIVO", "MODELAGEM VOLUMÉTRICA", "BASE NORMATIVA"])

# ------------------------------------------
# ABA 1: RESUMO EXECUTIVO
# ------------------------------------------
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if aprovado:
        # Caixa de Sucesso Customizada (Sem Emoji)
        st.markdown("""
        <div class='alerta-aprovado'>
            <div class='alerta-titulo'>STATUS: VIABILIDADE PRÉ-APROVADA</div>
            <div class='alerta-texto'>Os parâmetros do lote atendem a todas as restrições mínimas do Plano Diretor vigente.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas interativas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>Área do Terreno</div><div class='metric-value'>{area_terreno:,.0f} m²</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>Potencial (CA)</div><div class='metric-value'>{area_max_computavel:,.0f} m²</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>Capacidade</div><div class='metric-value'>{unidades_estimadas} uds</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>VGV Estimado</div><div class='metric-value'>R$ {vgv_estimado:,.0f}</div></div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos Analíticos
        col_graf_1, col_graf_2 = st.columns([1, 1])
        with col_graf_1:
            st.markdown("<h3 style='font-size: 15px; color: #0F172A; margin-bottom: 10px;'>DISTRIBUIÇÃO DE SOLO</h3>", unsafe_allow_html=True)
            fig_donut = go.Figure(data=[go.Pie(
                labels=['Área de Projeção Permitida', 'Área Permeável Obrigatória'],
                values=[area_ocupada_terreo, area_livre_terreo],
                hole=.6,
                marker_colors=['#2563EB', '#E2E8F0']
            )])
            fig_donut.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=250, paper_bgcolor='rgba(0,0,0,0)', showlegend=True)
            st.plotly_chart(fig_donut, use_container_width=True)
            
        with col_graf_2:
            st.markdown("<h3 style='font-size: 15px; color: #0F172A; margin-bottom: 10px;'>AÇÃO REQUERIDA</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #64748B; font-size: 14px; margin-bottom: 25px;'>A conformidade legal foi estabelecida. Gere o laudo técnico automático para documentação executiva do projeto.</p>", unsafe_allow_html=True)
            
            pdf_bytes = gerar_pdf_evtl()
            st.download_button(
                label="GERAR RELATÓRIO EVTL",
                data=pdf_bytes,
                file_name=f"EVTL_Aprova_AI_{cidade.split()[0]}.pdf",
                mime="application/pdf"
            )

    else:
        # Caixa de Erro Customizada (Sem Emoji)
        html_erros = "".join([f"<li>{erro}</li>" for erro in erros_normativos])
        st.markdown(f"""
        <div class='alerta-reprovado'>
            <div class='alerta-titulo'>STATUS: VIABILIDADE REPROVADA</div>
            <div class='alerta-texto'>
                Foi detectada inconformidade com a legislação urbanística:
                <ul style='margin-top: 8px; margin-bottom: 0px;'>{html_erros}</ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 14px; font-weight: 500;'>Reajuste as premissas geométricas no painel lateral para prosseguir.</p>", unsafe_allow_html=True)

# ------------------------------------------
# ABA 2: MODELAGEM VOLUMÉTRICA
# ------------------------------------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    if aprovado:
        st.markdown("<h3 style='font-size: 15px; color: #0F172A; text-transform: uppercase;'>ENVELOPE MÁXIMO EDIFICÁVEL</h3>", unsafe_allow_html=True)
        
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
                opacity=0.9, color='#2563EB', flatshading=True
            )
        ])
        
        fig_3d.add_trace(go.Mesh3d(
            x=[0, 0, largura, largura], y=[0, comprimento, comprimento, 0], z=[0, 0, 0, 0],
            i=[0, 0], j=[1, 2], k=[2, 3], opacity=0.08, color='#0F172A'
        ))

        fig_3d.update_layout(
            scene=dict(
                xaxis=dict(title='Testada (m)', backgroundcolor="#F4F7FB", gridcolor="#E2E8F0"),
                yaxis=dict(title='Profundidade (m)', backgroundcolor="#F4F7FB", gridcolor="#E2E8F0"),
                zaxis=dict(title='Altura Máx (m)', backgroundcolor="#F4F7FB", gridcolor="#E2E8F0"),
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='rgba(0,0,0,0)', height=550
        )
        st.plotly_chart(fig_3d, use_container_width=True)
    else:
        st.markdown("""
        <div class='alerta-reprovado' style='background-color: #F8FAFC; border-color: #CBD5E1;'>
            <div class='alerta-titulo' style='color: #64748B;'>VISUALIZAÇÃO BLOQUEADA</div>
            <div class='alerta-texto'>A modelagem espacial não pode ser gerada devido a infrações geométricas no dimensionamento do lote.</div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------
# ABA 3: BASE NORMATIVA
# ------------------------------------------
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    col_tab_1, col_tab_2 = st.columns([1.8, 1])
    
    with col_tab_1:
        st.markdown("<h3 style='font-size: 15px; color: #0F172A;'>DIRETRIZES LEGAIS APLICADAS</h3>", unsafe_allow_html=True)
        dados_tabela = {
            "DISPOSITIVO LEGAL": ["Área Mínima de Loteamento", "Testada Mínima Exigida", "Coeficiente de Aproveitamento (CA)", "Taxa de Ocupação Máxima (TO)", "Gabarito de Altura", "Recuo Frontal", "Recuo Lateral e Fundos"],
            "RESTRIÇÃO": [f"{regras['Lote_Minimo']} m²", f"{regras['Testada_Minima']} metros", f"{regras['CA']}x a área nominal", f"{regras['TO']*100:.0f}%", f"{regras['Gabarito']} metros", f"{regras['Recuo_Frontal']} metros", f"{regras['Recuo_Lateral']} metros"]
        }
        st.table(pd.DataFrame(dados_tabela))
        
    with col_tab_2:
        st.markdown("<h3 style='font-size: 15px; color: #0F172A;'>CÓDIGO DE ORIGEM</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 14px;'>Acesse a regulamentação completa para análise de outorgas ou exceções construtivas.</p>", unsafe_allow_html=True)
        
        nome_arquivo = "Plano Diretor - Navegantes.pdf"
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, "rb") as file:
                st.download_button(label="DOWNLOAD DOCUMENTO MATRIZ", data=file, file_name=nome_arquivo, mime="application/pdf")
        else:
            st.markdown(f"""
            <div class='alerta-reprovado' style='background-color: #FFFBEB; border-color: #F59E0B;'>
                <div class='alerta-titulo' style='color: #B45309;'>ARQUIVO AUSENTE</div>
                <div class='alerta-texto'>O arquivo base '{nome_arquivo}' não foi detectado no banco de dados.</div>
            </div>
            """, unsafe_allow_html=True)

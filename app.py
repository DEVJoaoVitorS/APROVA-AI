import streamlit as st
import pandas as pd
import os

# 1. CONFIGURAÇÃO DA PÁGINA (Fica em tela cheia)
st.set_page_config(page_title="Aprova AI | Parâmetros Urbanísticos", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# INJEÇÃO DE CSS CUSTOMIZADO (ESTÉTICA GO.ARCH)
# ==========================================
estilo_customizado = """
<style>
    /* Importando a fonte elegante Montserrat do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

    /* Forçando a fonte e o fundo escuro em todo o app */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    .stApp {
        background-color: #1a1a1a !important; /* Cinza muito escuro/Quase preto */
        color: #e0e0e0 !important; /* Texto cinza claro para não cansar a vista */
    }
    
    /* Estilizando a barra lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #111111 !important; /* Preto profundo */
        border-right: 1px solid #333333 !important;
    }
    
    /* Títulos e Subtítulos em Dourado/Cobre */
    h1, h2, h3 {
        color: #C5A059 !important; /* Tom dourado da imagem de referência */
        font-weight: 600 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    
    /* Caixas de seleção (Selectbox) */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #222222 !important;
        border: 1px solid #C5A059 !important;
        color: #ffffff !important;
        border-radius: 0px !important; /* Bordas retas e modernas */
    }
    
    /* Botões de Download */
    .stDownloadButton>button {
        background-color: transparent !important;
        color: #C5A059 !important;
        border: 1px solid #C5A059 !important;
        border-radius: 0px !important; /* Bordas retas */
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        width: 100%;
    }
    
    /* Efeito ao passar o mouse no botão */
    .stDownloadButton>button:hover {
        background-color: #C5A059 !important;
        color: #111111 !important;
    }
    
    /* Estilização da Tabela de Restrições */
    [data-testid="stTable"] {
        background-color: #222222 !important;
    }
    [data-testid="stTable"] th {
        background-color: #111111 !important;
        color: #C5A059 !important;
        border-bottom: 2px solid #C5A059 !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
    }
    [data-testid="stTable"] td {
        border-bottom: 1px solid #333333 !important;
        color: #e0e0e0 !important;
    }

    /* Caixa de Resumo Customizada */
    .resumo-box {
        background-color: #222222;
        padding: 20px;
        border-left: 4px solid #C5A059;
        margin-bottom: 30px;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Linhas divisórias */
    hr {
        border-color: #333333 !important;
    }
</style>
"""
st.markdown(estilo_customizado, unsafe_allow_html=True)

# ==========================================
# CÓDIGO PRINCIPAL DO SITE
# ==========================================

# 2. CABEÇALHO DO SITE
st.title("APROVA AI")
st.markdown("<p style='font-size: 18px; letter-spacing: 1px; color: #a0a0a0;'>INTELIGÊNCIA EM PARÂMETROS URBANÍSTICOS</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. BANCO DE DADOS ESTRUTURADO
banco_dados = {
    "Itajaí - SC": {
        "Resumo": "Parâmetros gerais baseados na Lei Complementar 449/2024. Foco em verticalização e controle de fachada ativa.",
        "parametros": {
            "Recuo Frontal Embasamento": "Geralmente 4,00m (Permite avanço de sacada em balanço até 1,20m)",
            "Recuo Frontal Torre": "Mínimo de 4,00m (Garantir que não seja menor que o embasamento)",
            "Taxa de Ocupação (TO)": "Base: Até 70% | Torre: Acréscimo de até 10% permitido com outorga",
            "Tamanho Mín. Quartos": "Quarto principal: Mínimo 9,00m² | Demais quartos: Mínimo 7,50m²",
            "Vagas de Garagem": "Mínimo de 1 vaga por unidade (Consultar variação por zona específica)"
        },
        "arquivos": ["Código de Obras Itajaí.pdf", "Plano Diretor Itajaí.pdf"]
    },
    "Navegantes - SC": {
        "Resumo": "Parâmetros aplicáveis para as principais zonas residenciais de Navegantes. Atenção especial aos recuos em áreas de expansão.",
        "parametros": {
            "Recuo Frontal Embasamento": "Mínimo de 3,00m a 4,00m (Depende do viário)",
            "Recuo Frontal Torre": "Mínimo de 4,00m a partir do 3º pavimento",
            "Taxa de Ocupação (TO)": "Até 60% na base e 40% a 50% na torre",
            "Tamanho Mín. Quartos": "Mínimo de 9,00m² (Quarto 1) e 7,50m² (Quartos extras)",
            "Vagas de Garagem": "1 vaga por apartamento (Até 2 quartos) / 2 vagas (3+ quartos)"
        },
        "arquivos": ["Plano Diretor - Navegantes.pdf"] 
    }
}

# 4. BARRA DE PESQUISA (INTERFACE LATERAL)
st.sidebar.markdown("<h3>FILTRO DE BUSCA</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #a0a0a0; font-size: 14px;'>Selecione o município para extrair os parâmetros construtivos consolidados.</p>", unsafe_allow_html=True)
cidade_escolhida = st.sidebar.selectbox("", [""] + list(banco_dados.keys()))

# 5. EXIBIÇÃO DOS DADOS NA TELA
if cidade_escolhida != "":
    dados = banco_dados[cidade_escolhida]
    
    st.markdown(f"<h2>📍 {cidade_escolhida.upper()}</h2>", unsafe_allow_html=True)
    
    # Exibe o resumo na nossa caixa customizada estilosa
    st.markdown(f"<div class='resumo-box'>{dados['Resumo']}</div>", unsafe_allow_html=True)
    
    # Criando colunas para dividir a tela e deixar mais arquitetônico
    col1, padding, col2 = st.columns([1.5, 0.1, 1])
    
    with col1:
        st.markdown("<h3>📊 RESTRIÇÕES BÁSICAS</h3>", unsafe_allow_html=True)
        df_parametros = pd.DataFrame(list(dados["parametros"].items()), columns=["DIRETRIZ", "PARÂMETRO TÉCNICO"])
        st.table(df_parametros)
        
    with col2:
        st.markdown("<h3>📥 DOCUMENTAÇÃO</h3>", unsafe_allow_html=True)
        st

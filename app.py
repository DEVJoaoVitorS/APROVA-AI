import streamlit as st
import pandas as pd
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Aprova AI | Parâmetros Urbanísticos", layout="wide")

# 2. CABEÇALHO DO SITE
st.title("🏗️ Aprova AI")
st.subheader("Consulta Rápida de Parâmetros Urbanísticos e Códigos de Obras")
st.markdown("---")

# 3. BANCO DE DADOS ESTRUTURADO
banco_dados = {
    "Itajaí - SC": {
        "Resumo": "Parâmetros gerais baseados na Lei Complementar 449/2024.",
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
        "Resumo": "Parâmetros aplicáveis para as principais zonas residenciais de Navegantes.",
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

# 4. BARRA DE PESQUISA (INTERFACE)
st.sidebar.header("Filtro de Busca")
cidade_escolhida = st.sidebar.selectbox("Selecione a cidade para análise:", [""] + list(banco_dados.keys()))

# 5. EXIBIÇÃO DOS DADOS NA TELA
if cidade_escolhida != "":
    dados = banco_dados[cidade_escolhida]
    
    st.header(f"📍 Parâmetros para {cidade_escolhida}")
    st.write(dados["Resumo"])
    
    # Exibir a Tabela de Parâmetros
    st.subheader("📊 Tabela de Restrições Básicas")
    df_parametros = pd.DataFrame(list(dados["parametros"].items()), columns=["Item", "Regra/Exigência"])
    st.table(df_parametros)
    
    # Área de Download dos PDFs Originais
    st.markdown("---")
    st.subheader("📥 Documentação Original")
    st.write("Baixe as leis e normas completas para validação em profundidade:")
    
    # Cria os botões de download dinamicamente se o arquivo existir no GitHub
    for nome_arquivo in dados["arquivos"]:
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, "rb") as file:
                btn = st.download_button(
                    label=f"Baixar {nome_arquivo}",
                    data=file,
                    file_name=nome_arquivo,
                    mime="application/pdf"
                )
        else:
            st.warning(f"O arquivo {nome_arquivo} ainda não foi enviado para a plataforma.")
else:
    st.info("👈 Selecione uma cidade na barra lateral para começar a análise de viabilidade.")

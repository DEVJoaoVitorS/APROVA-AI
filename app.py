import streamlit as st
import pandas as pd
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Aprova AI | Parâmetros Urbanísticos", layout="wide")

# 2. CABEÇALHO DO SITE
st.title("🏗️ Aprova AI")
st.subheader("Consulta Rápida de Parâmetros Urbanísticos e Códigos de Obras")
st.markdown("---")

# 3. BANCO DE DADOS ESTRUTURADO (A "Opção A" que você escolheu)
# Aqui é onde você vai colocar os resumos que a IA extraiu no Colab
banco_dados = {
    "Itajaí - SC": {
        "Resumo": "Parâmetros gerais baseados na Lei Complementar 449/2024.",
        "parametros": {
            "Recuo Frontal Embasamento": "Depende da via (Ver Anexo 2)",
            "Recuo Frontal Torre": "Avanço permitido de até 1,20m em balanço",
            "Taxa de Ocupação (TO)": "Subsolo igual ao embasamento (Art. 122)",
            "Tamanho Mín. Quartos": "Conforme NBR 15575 / Código Obras",
            "Vagas de Garagem": "Consultar Tabela de Zoneamento"
        },
        "arquivos": ["Código de Obras Itajaí.pdf", "Plano Diretor Itajaí.pdf"]
    },
    "Navegantes - SC": {
        "Resumo": "Parâmetros gerais baseados na legislação vigente de Navegantes.",
        "parametros": {
            "Recuo Frontal Embasamento": "Consultar Zoneamento Local",
            "Recuo Frontal Torre": "Consultar Zoneamento Local",
            "Taxa de Ocupação (TO)": "Consultar Zoneamento Local",
            "Tamanho Mín. Quartos": "Conforme Código de Obras Local",
            "Vagas de Garagem": "Consultar Tabela Específica"
        },
        "arquivos": ["Plano_Diretor_Navegantes.pdf"] # Ajuste o nome conforme o PDF que você subiu
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

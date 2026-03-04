import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Navegação com Menu", layout="wide")

# Menu lateral
with st.sidebar:
    pagina = option_menu(
        "Menu",
        ["Home", "Sobre", "Contato", "Projeto", 
         "Fatura MES 03",
         "Fatura Mês 04",
         ],
        icons=["house", "info", "envelope", "file-earmark-code", "database", "database", "database"],
        menu_icon="cast",
        default_index=0
    )


# Página: Home
if pagina == "Home":
    st.title("Página Inicial")
    st.write("Bem-vindo!")
# Página: Sobre
elif pagina == "Sobre":
    st.title("Sobre")
    st.write("Informações sobre o projeto.")

# Página: Contato
elif pagina == "Contato":
    st.title("Contato")
    st.write("Envie-nos uma mensagem.")


# PAGAINA PROJETO CARTAO_CREDDITO

elif pagina == "Fatura MES 03":
    st.title("Fatura MES 03")
    st.write("Vamos ver como está sua fatura")

    # carregando os dados 
    df = pd.read_excel("Nubank_Mes_03.xlsx")
    
    #exibir dados 
    st.dataframe(df)

    # graficos

    # Gráfico interativo com escolha de colunas
    colunas = df.columns
    x_col = st.selectbox("Selecione a coluna para o eixo X", colunas)
    y_col = st.selectbox("Selecione a coluna para o eixo Y", colunas)

    if x_col and y_col:
        fig = px.line(df, x=x_col, y=y_col, title=f"Gráfico de {x_col} vs {y_col}")
        st.plotly_chart(fig)
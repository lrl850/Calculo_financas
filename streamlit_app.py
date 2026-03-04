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
         "Curso Integrado em Informática",
         
        icons=["house", "info", "envelope", "file-earmark-code", "database", "database", "database"],
        menu_icon="cast",
        default_index=0
    )


# Página: Home
if pagina == "Home":
    st.title("Página Inicial")
    st.write("Bem-vindo!")

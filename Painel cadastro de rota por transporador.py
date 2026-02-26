import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# =========================
# ESCOLHA DE TEMA
# =========================
tema = st.sidebar.selectbox(
    "Escolha o Tema",
    ["Corporativo Azul", "Escuro Premium", "Claro Minimalista"]
)

if tema == "Corporativo Azul":
    cor_fundo = "#1f4e79"
    cor_card = "#1e1e1e"
    cor_header = "#1f4e79"
    cor_texto = "#ffffff"

elif tema == "Escuro Premium":
    cor_fundo = "#0f2027"
    cor_card = "#1e1e1e"
    cor_header = "#26276d"
    cor_texto = "#ffffff"

else:
    cor_fundo = "#ffffff"
    cor_card = "#1f4e79"
    cor_header = "#4CAF50"
    cor_texto = "#A7A4A465"

st.markdown(f"""
<style>
.stApp {{
    background-color: {cor_fundo};
}}

h1, h2, h3, label {{
    color: {cor_texto} !important;
}}

.card {{
    background-color: {cor_card};
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    text-align: center;
}}

thead tr th {{
    background-color: {cor_header} !important;
    color: white !important;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# CARREGAR PLANILHA
# =========================
arquivo = "Planilha de cadastro de prazos por rota.xlsx"
df = pd.read_excel(arquivo, sheet_name="Planilha1")
df.columns = df.columns.str.strip()
df = df.dropna(axis=1, how='all')
df = df.loc[:, ~df.columns.str.contains("Unnamed", case=False)]

# =========================
# TÍTULO
# =========================
st.markdown("<h1>Sistema Logístico - Cadastro de Rotas</h1>", unsafe_allow_html=True)

# =========================
# FILTRO LATERAL (ERP)
# =========================
st.sidebar.header("Filtros")

transportadora = st.sidebar.multiselect(
    "Transportadora",
    df["Transportadora"].unique()
)

estado = st.sidebar.multiselect(
    "Estado",
    df["Estado"].unique()
)

df_filtrado = df.copy()

if transportadora:
    df_filtrado = df_filtrado[df_filtrado["Transportadora"].isin(transportadora)]

if estado:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estado)]

# =========================
# DASHBOARD KPIs
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='card'><h3>Total Registros</h3><h2>{len(df_filtrado)}</h2></div>", unsafe_allow_html=True)

with col2:
    total_transportadoras = df_filtrado["Transportadora"].nunique()
    st.markdown(f"<div class='card'><h3>Transportadoras</h3><h2>{total_transportadoras}</h2></div>", unsafe_allow_html=True)

with col3:
    total_estados = df_filtrado["Estado"].nunique()
    st.markdown(f"<div class='card'><h3>Estados</h3><h2>{total_estados}</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# TABELA
# =========================

st.dataframe(df_filtrado, use_container_width=True)

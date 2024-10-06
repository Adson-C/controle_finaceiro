import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Função para calcular o saldo total
def saldo_total(df_receitas, df_despesas):
    valor = df_receitas["Valor"].sum() - df_despesas["Valor"].sum()
    return f'R$ {valor}'

# Função para carregar os dados
def load_data():
    df_receitas = pd.read_csv('df_receitas.csv')
    df_despesas = pd.read_csv('df_despesas.csv')
    return df_receitas, df_despesas

# Carregar dados
df_receitas, df_despesas = load_data()

# Layout da página
st.set_page_config(
     page_title="Home",
    page_icon="💸",
    layout="wide"
    )

# Cabeçalho do dashboard
st.title("Controle Financeiro")
st.sidebar.markdown("Desenvolvido por: [Adson](https://github.com/Adson-C?tab=repositories)")

# Linha 1: Blocos para Saldo, Receita e Despesa
col1, col2, col3 = st.columns(3)

with col1:
    saldo = saldo_total(df_receitas, df_despesas)
    st.markdown(f"<h3 style='color: green;'>Saldo</h3><h4 style='color: green;'>{saldo}</h4>", unsafe_allow_html=True)

with col2:
    receita = f"R$ {df_receitas['Valor'].sum()}"
    st.markdown(f"<h3 style='color: blue;'>Receita</h3><h4 style='color: blue;'>{receita}</h4>", unsafe_allow_html=True)

with col3:
    despesa = f"R$ {df_despesas['Valor'].sum()}"
    st.markdown(f"<h3 style='color: red;'>Despesa</h3><h4 style='color: red;'>{despesa}</h4>", unsafe_allow_html=True)

# # Linha 2: Filtros e gráficos
# st.subheader("Filtrar lançamentos")

# # Filtros de categoria
# categoria_receitas = st.multiselect("Categorias das receitas", options=df_receitas['Categoria'].unique())
# categoria_despesas = st.multiselect("Categorias das despesas", options=df_despesas['Categoria'].unique())

# Filtro de período de análise
# data_inicio = st.date_input("Data de início", datetime(2024, 1, 1))
# data_fim = st.date_input("Data de fim", datetime(2024, 12, 31))

# Aplicar filtros
# if categoria_receitas:
#     df_receitas = df_receitas[df_receitas['Categoria'].isin(categoria_receitas)]
# if categoria_despesas:
#     df_despesas = df_despesas[df_despesas['Categoria'].isin(categoria_despesas)]

# df_receitas = df_receitas[(df_receitas['Data'] >= pd.to_datetime(data_inicio)) & 
#                           (df_receitas['Data'] <= pd.to_datetime(data_fim))]
# df_despesas = df_despesas[(df_despesas['Data'] >= pd.to_datetime(data_inicio)) & 
#                           (df_despesas['Data'] <= pd.to_datetime(data_fim))]

# Gráficos
st.subheader("Gráficos de Receitas e Despesas")

col4, col5 = st.columns(2)
# 'Plotly': color_discrete_sequence=px.colors.qualitative.Plotly
# 'D3': color_discrete_sequence=px.colors.qualitative.D3
# 'G10': color_discrete_sequence=px.colors.qualitative.G10
with col4:
    fig_receitas = px.bar(df_receitas, x='Categoria', y='Valor', title="Receitas por Categoria", 
                          color='Categoria', color_discrete_sequence=px.colors.qualitative.D3)
    st.plotly_chart(fig_receitas)

with col5:
    fig_despesas = px.pie(df_despesas, values='Valor', names='Categoria', title="Distribuição de Despesas",
                          color='Categoria', color_discrete_sequence=px.colors.qualitative.G10)
    st.plotly_chart(fig_despesas)

# Exibir o DataFrame combinado como resumo
st.subheader('Resumo Total')
df_combined = pd.concat([df_receitas, df_despesas])
st.dataframe(df_combined)


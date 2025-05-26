import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Dashboard de Usuários para Remarketing")

df = pd.read_csv('dados/dados_usuarios_remarketing.csv')

st.sidebar.header("Filtros")
categoria = st.sidebar.selectbox("Filtrar por Categoria", ["Todas"] + sorted(df['top_category'].dropna().unique().tolist()))

if categoria != "Todas":
    df = df[df['top_category'] == categoria]

col1, col2 = st.columns(2)

with col1:
    st.metric("Usuários Elegíveis", df['flag_remarketing'].sum())
    fig1 = px.histogram(df, x='n_views', nbins=30, title="Distribuição de Visualizações")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.box(df, y='dias_ativos', title="Distribuição de Dias Ativos")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 📦 Categorias Mais Frequentes entre Elegíveis")
df_elig = df[df['flag_remarketing'] == 1]
st.dataframe(df_elig['top_category'].value_counts().head(10).reset_index().rename(columns={'index': 'Categoria', 'top_category': 'Contagem'}))


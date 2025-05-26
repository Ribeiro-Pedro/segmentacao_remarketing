# ecommerce_dashboard_v1.py

import pandas as pd
from google.cloud import bigquery
import streamlit as st
import plotly.express as px

# Configuração do Streamlit
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")
st.title("Dashboard Analítico de E-commerce")

# Função para carregar dados do BigQuery
@st.cache_data(show_spinner=True)
def carregar_dados():
    client = bigquery.Client()
    query = """
        SELECT
            event_date,
            event_name,
            user_pseudo_id,
            geo.country,
            traffic_source.source AS traffic_source,
            device.category AS device_category,
            ecommerce.total_item_quantity,
            ecommerce.purchase_revenue_in_usd
        FROM
            `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
        WHERE
            _TABLE_SUFFIX BETWEEN '20210101' AND '20210131'
            AND event_name IN ('purchase', 'add_to_cart', 'view_item', 'begin_checkout')
    """
    return client.query(query).to_dataframe()

# Carregar dados
df = carregar_dados()

# Conversão de tipos
df['event_date'] = pd.to_datetime(df['event_date'], format='%Y%m%d')

# Filtros laterais
with st.sidebar:
    st.header("Filtros")
    data_inicial = st.date_input("Data inicial", df['event_date'].min())
    data_final = st.date_input("Data final", df['event_date'].max())
    canais = st.multiselect("Fonte de tráfego", df['traffic_source'].dropna().unique(), default=None)

# Aplicar filtros
mask = (df['event_date'] >= pd.to_datetime(data_inicial)) & (df['event_date'] <= pd.to_datetime(data_final))
if canais:
    mask &= df['traffic_source'].isin(canais)
df_filtrado = df[mask]

# KPIs principais
col1, col2, col3 = st.columns(3)
col1.metric("Total de Sessões", df_filtrado['user_pseudo_id'].nunique())
col2.metric("Total de Compras", df_filtrado[df_filtrado['event_name'] == 'purchase'].shape[0])
col3.metric("Receita Total (USD)", round(df_filtrado['purchase_revenue_in_usd'].sum(), 2))

# Gráfico de eventos ao longo do tempo
df_eventos = df_filtrado.groupby(['event_date', 'event_name']).size().reset_index(name='count')
fig_eventos = px.line(df_eventos, x='event_date', y='count', color='event_name', title="Eventos por data")
st.plotly_chart(fig_eventos, use_container_width=True)

# Distribuição por dispositivo
df_dispositivo = df_filtrado.groupby(['device_category']).size().reset_index(name='count')
fig_device = px.pie(df_dispositivo, names='device_category', values='count', title="Distribuição por dispositivo")
st.plotly_chart(fig_device, use_container_width=True)

# Receita por país
df_receita = df_filtrado[df_filtrado['event_name'] == 'purchase']
df_receita_pais = df_receita.groupby('country')['purchase_revenue_in_usd'].sum().reset_index()
fig_receita = px.bar(df_receita_pais.sort_values(by='purchase_revenue_in_usd', ascending=False).head(10),
                     x='country', y='purchase_revenue_in_usd', title="Top 10 países por receita")
st.plotly_chart(fig_receita, use_container_width=True)

st.caption("Fonte: Google Analytics 4 Sample Dataset - BigQuery")

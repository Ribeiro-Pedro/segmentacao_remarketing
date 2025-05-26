import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# --- Carregar dados ---
@st.cache_data
def load_data():
    return pd.read_csv('ecommerce_dashboard/data/ecommerce_data_preprocessed.csv', parse_dates=['event_date'])

df = load_data()

st.title("E-commerce Dashboard - GA4")

# --- Sidebar: Filtros ---
st.sidebar.header("Filtros")

# ✅ Filtro por intervalo de datas
min_date = df['event_date'].min()
max_date = df['event_date'].max()

date_range = st.sidebar.date_input(
    "Selecione o intervalo de datas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# ✅ Filtro por canal (traffic_source)
traffic_sources = df['traffic_source'].dropna().unique().tolist()
selected_channels = st.sidebar.multiselect(
    "Selecione o(s) canal(is) de aquisição",
    options=traffic_sources,
    default=traffic_sources  # seleciona todos por padrão
)

# ✅ Filtro por tipo de evento
event_types = df['event_name'].dropna().unique().tolist()
selected_events = st.sidebar.multiselect(
    "Selecione o(s) tipo(s) de evento",
    options=event_types,
    default=event_types  # seleciona todos por padrão
)

# ✅ Aplicar filtros
if isinstance(date_range, tuple):
    df = df[(df['event_date'] >= pd.to_datetime(date_range[0])) & 
            (df['event_date'] <= pd.to_datetime(date_range[1]))]

if selected_channels:
    df = df[df['traffic_source'].isin(selected_channels)]

if selected_events:
    df = df[df['event_name'].isin(selected_events)]

st.write(f"Período selecionado: {date_range[0]} até {date_range[1]}")
st.write(f"Total de eventos após filtros: {len(df)}")

# --- Pré-processamento ---
# Identificar visitantes únicos que realizaram compras
compradores = df[df['event_name'] == 'purchase']['user_pseudo_id'].nunique()
visitantes = df['user_pseudo_id'].nunique()

taxa_conversao = (compradores / visitantes) * 100 if visitantes > 0 else 0

# Compras por mês
df['month'] = df['event_date'].dt.to_period('M')
compras = df[df['event_name'] == 'purchase']
compras_por_mes = compras.groupby(['user_pseudo_id', 'month']).size().reset_index(name='compras')

# Tamanho médio do carrinho
tamanho_carrinho = compras['purchase_revenue_in_usd'].mean() if not compras.empty else 0

# Taxa de abandono: usuários que começaram checkout mas não compraram
checkout_users = df[df['event_name'] == 'begin_checkout']['user_pseudo_id'].unique()
compradores_users = compras['user_pseudo_id'].unique()
abandono = len(set(checkout_users) - set(compradores_users))
taxa_abandono = (abandono / len(checkout_users)) * 100 if len(checkout_users) > 0 else 0

# Receita por cliente (LTV estimado)
if not compras.empty:
    receita_cliente = compras.groupby('user_pseudo_id')['purchase_revenue_in_usd'].sum()
    ltv_medio = receita_cliente.mean()
else:
    ltv_medio = 0

# Principais fontes de tráfego
novos_visitantes = df.groupby('traffic_source')['user_pseudo_id'].nunique().sort_values(ascending=False)

# --- Dashboard ---
st.header("Métricas principais")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Taxa de Conversão (%)", f"{taxa_conversao:.2f}")
with col2:
    st.metric("Tamanho Médio do Carrinho ($)", f"{tamanho_carrinho:.2f}")
with col3:
    st.metric("Taxa de Abandono (%)", f"{taxa_abandono:.2f}")

st.subheader("Compras por Mês")
if not compras_por_mes.empty:
    compras_por_mes_plot = compras_por_mes.groupby('month')['compras'].sum().reset_index()
    compras_por_mes_plot['month'] = compras_por_mes_plot['month'].astype(str)

    fig = px.bar(compras_por_mes_plot, x='month', y='compras', title='Compras por Mês')
    fig.update_layout(xaxis_tickangle=-90)
    st.plotly_chart(fig)
else:
    st.write("Sem compras no período selecionado.")

st.subheader("Lifetime Value (Médio) por Cliente")
st.write(f"US$ {ltv_medio:.2f}")

st.subheader("Principais Fontes de Tráfego")
if not novos_visitantes.empty:
    novos_visitantes_df = novos_visitantes.reset_index()
    novos_visitantes_df.columns = ['traffic_source', 'unique_users']

    fig_traf = px.bar(novos_visitantes_df, x='traffic_source', y='unique_users', title='Principais Fontes de Tráfego')
    st.plotly_chart(fig_traf)
else:
    st.write("Sem dados de visitantes no período selecionado.")
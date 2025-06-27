import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile 
import os

# Configuração básica da página
st.set_page_config(page_title="Dashboard: Brazilian E-Commerce Public Dataset", page_icon="🇧🇷", layout="wide")

# Título e introdução
st.title('Análise de Dados sobre o Comércio digital no Brasil🇧🇷')
st.markdown("O dataset 'Brazilian E-Commerce Public Dataset by Olist' contém informações de mais de 100 mil pedidos realizados entre 2016 e 2018.")

@st.cache_data
def carregar_dados():
    base = 'dados/'

    orders = pd.read_csv(base + 'olist_orders_dataset.csv')
    customers = pd.read_csv(base + 'olist_customers_dataset.csv')
    order_items = pd.read_csv(base + 'olist_order_items_dataset.csv')
    order_payments = pd.read_csv(base + 'olist_order_payments_dataset.csv')
    order_reviews = pd.read_csv(base + 'olist_order_reviews_dataset.csv')
    products = pd.read_csv(base + 'olist_products_dataset.csv')
    sellers = pd.read_csv(base + 'olist_sellers_dataset.csv')
    category_translation = pd.read_csv(base + 'product_category_name_translation.csv')

    return orders, customers, order_items, order_payments, order_reviews, products, sellers, category_translation

# Carrega os dados
orders, customers, order_items, order_payments, order_reviews, products, sellers, category_translation = carregar_dados()

# Interface
col1, col2, col3 = st.columns(3)
col1.metric("Total de Pedidos", len(orders))
col2.metric("Clientes Únicos", customers["customer_unique_id"].nunique())
col3.metric("Total de Vendedores", sellers["seller_id"].nunique())

# --- Gráfico 1: Pedidos por estado ---
pedidos_estado = orders.merge(customers, on='customer_id')
pedidos_estado = pedidos_estado['customer_state'].value_counts().reset_index()
pedidos_estado.columns = ['Estado', 'Total de Pedidos']

fig1 = px.bar(
    pedidos_estado,
    x='Estado',
    y='Total de Pedidos',
    title="Total de Pedidos por Estado",
    color_discrete_sequence=["lightskyblue"]
)

# --- Gráfico 2: Pedidos por mês ---
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
pedidos_mes = orders.set_index('order_purchase_timestamp').resample('M').order_id.count().reset_index()
pedidos_mes.columns = ['Data', 'Total de Pedidos']

fig2 = px.line(
    pedidos_mes,
    x='Data',
    y='Total de Pedidos',
    title="Evolução Mensal de Pedidos",
    markers=True,
    color_discrete_sequence=["lightskyblue"]
)

st.subheader("📊 Visão Geral de Pedidos")
col1, col2 = st.columns(2)
with col1:
    st.write("### Total de Pedidos por Estado")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.write("### Evolução Mensal de Pedidos")
    st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico 3: Violin Plot ---
orders_reviews = orders.merge(order_reviews[['order_id', 'review_score']], on='order_id')
orders_reviews['order_purchase_timestamp'] = pd.to_datetime(orders_reviews['order_purchase_timestamp'])
orders_reviews['order_delivered_customer_date'] = pd.to_datetime(orders_reviews['order_delivered_customer_date'])
orders_reviews['delivery_days'] = (orders_reviews['order_delivered_customer_date'] - orders_reviews['order_purchase_timestamp']).dt.days

fig3 = px.violin(
    orders_reviews,
    x='review_score',
    y='delivery_days',
    box=True,
    points="all",
    color='review_score',
    title='Distribuição dos Dias de Entrega por Nota de Avaliação'
)
fig3.update_layout(showlegend=False)

# --- Gráfico 4: Pagamento + Parcelas ---
pagamentos = order_payments['payment_type'].value_counts().reset_index()
pagamentos.columns = ['Tipo de Pagamento', 'Quantidade']

fig4 = px.pie(
    pagamentos,
    names='Tipo de Pagamento',
    values='Quantidade',
    title='Distribuição dos Tipos de Pagamento',
    color_discrete_sequence=px.colors.sequential.Blues
)

# Layout linha 2
col3, col4 = st.columns(2)

with col3:
    st.write("### Dias de Entrega por Nota de Avaliação")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.write("### Tipos de Pagamento")
    st.plotly_chart(fig4, use_container_width=True)

    mostrar_parcelas = st.checkbox("Clique para visualizar detalhes do parcelamento no cartão de crédito")

    if mostrar_parcelas:
        parcelas = order_payments[order_payments['payment_type'] == 'credit_card']
        parcelas = parcelas[parcelas['payment_installments'] <= 12]  # Limita até 12 parcelas
        parcelas_agrupadas = parcelas['payment_installments'].value_counts().reset_index()
        parcelas_agrupadas.columns = ['Parcelas', 'Quantidade']
        parcelas_agrupadas = parcelas_agrupadas.sort_values('Parcelas')

        fig_parcelas = px.bar(
            parcelas_agrupadas,
            x='Parcelas',
            y='Quantidade',
            title='Distribuição de Parcelas para Cartão de Crédito',
            color='Parcelas',
            color_discrete_sequence=px.colors.sequential.Blues
        )
        fig_parcelas.update_layout(bargap=0.2)
        st.plotly_chart(fig_parcelas, use_container_width=True)

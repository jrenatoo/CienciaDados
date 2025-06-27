import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import zipfile 
import os


# Configuração básica da página
st.set_page_config(page_title="Dashboard: Brazilian E-Commerce Public Dataset", page_icon="🇧🇷")

# Título e introdução
st.title('Análise de Dados sobre o Comércio digital no Brasil')
st.markdown("O dataset 'Brazilian E-Commerce Public Dataset by Olist' contém informações de mais de 100 pedidos realizados entre 2016 e 2018.")


st.set_page_config(page_title="Dashboard Olist", layout="wide")

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

# Exibe tabela inicial
st.subheader("Pedidos")
st.dataframe(orders.head())

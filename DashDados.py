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

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    zip_path = 'dados/olist_dataset.zip'
    extract_path = 'dados/extraidos'

    os.makedirs(extract_path, exist_ok=True)

    # Extrai os arquivos (independente da estrutura interna)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Função para encontrar o caminho correto dos arquivos
    def encontrar(nome_arquivo):
        for root, dirs, files in os.walk(extract_path):
            for file in files:
                if file == nome_arquivo:
                    return os.path.join(root, file)
        raise FileNotFoundError(f'{nome_arquivo} não encontrado dentro do .zip extraído.')

    # Carregar cada CSV pelo caminho correto
    orders = pd.read_csv(encontrar('olist_orders_dataset.csv'))
    customers = pd.read_csv(encontrar('olist_customers_dataset.csv'))
    order_items = pd.read_csv(encontrar('olist_order_items_dataset.csv'))
    order_payments = pd.read_csv(encontrar('olist_order_payments_dataset.csv'))
    order_reviews = pd.read_csv(encontrar('olist_order_reviews_dataset.csv'))
    products = pd.read_csv(encontrar('olist_products_dataset.csv'))
    sellers = pd.read_csv(encontrar('olist_sellers_dataset.csv'))
    category_translation = pd.read_csv(encontrar('product_category_name_translation.csv'))

    return orders, customers, order_items, order_payments, order_reviews, products, sellers, category_translation


orders, customers, order_items, order_payments, order_reviews, products, sellers, category_translation = carregar_dados()

st.metric("Total de pedidos", len(orders))
st.metric("Total de clientes", len(customers['customer_unique_id'].unique()))

orders_customers = orders.merge(customers, on='customer_id')
estado_counts = orders_customers['customer_state'].value_counts()

st.bar_chart(estado_counts)

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
pedidos_mes = orders.set_index('order_purchase_timestamp').resample('M').order_id.count()

st.line_chart(pedidos_mes)

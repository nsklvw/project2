import streamlit as st
import pandas as pd

st.set_page_config(page_title="Визуализация данных", layout="wide")

st.title("📊 Визуализация данных")

uploaded_file = st.sidebar.file_uploader("Загрузите CSV-файл", type=["csv"], key="sidebar_file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    if 'revenue' in df.columns:
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    st.session_state['df'] = df

if 'df' in st.session_state:
    df = st.session_state['df']

    st.subheader("1. Выручка по категориям товаров")
    if 'category' in df.columns and 'revenue' in df.columns:
        st.bar_chart(df.groupby('category')['revenue'].sum())

    st.subheader("2. Динамика продаж по месяцам")
    if 'order_date' in df.columns and 'revenue' in df.columns:
        monthly = df.set_index('order_date').resample('ME')['revenue'].sum().reset_index()
        monthly['order_date'] = monthly['order_date'].dt.strftime('%Y-%m')
        st.line_chart(monthly.set_index('order_date'))

    st.subheader("3. Распределение стоимости заказов")
    if 'revenue' in df.columns:
        st.bar_chart(df['revenue'])

    st.subheader("4. Распределение способов оплаты")
    if 'payment_method' in df.columns:
        st.bar_chart(df['payment_method'].value_counts())

    st.subheader("5. Топ-5 клиентов по сумме покупок")
    if 'customer_name' in df.columns and 'revenue' in df.columns:
        top_cust = df.groupby('customer_name')['revenue'].sum().sort_values(ascending=False).head(5)
        st.bar_chart(top_cust)

else:
    st.warning("Сначала загрузите CSV-файл")
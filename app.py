import streamlit as st
import pandas as pd

st.set_page_config(page_title="Анализ данных интернет-магазина", layout="wide")

st.title("🛒 Анализ данных интернет-магазина")

uploaded_file = st.sidebar.file_uploader("Загрузите CSV-файл", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
    df = df.drop_duplicates()
    
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    if 'revenue' in df.columns:
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
        df = df.dropna(subset=['revenue'])

    st.session_state['df'] = df
    st.success("Данные успешно загружены!")

    st.subheader("📋 Таблица данных")
    st.dataframe(df.head())

    st.subheader("📈 Результаты анализа")

    st.markdown("### 2.1. Самые популярные товары")
    if 'product_name' in df.columns and 'quantity' in df.columns:
        st.write(df.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(5))
        st.info("**Вывод:** Позиции, которые покупают чаще всего по количеству штук. Важно держать их в наличии.")

    st.markdown("### 2.2. Категории с наибольшей выручкой")
    if 'category' in df.columns and 'revenue' in df.columns:
        st.write(df.groupby('category')['revenue'].sum().sort_values(ascending=False))
        st.info("**Вывод:** Товарные категории, приносящие основной доход.")

    st.markdown("### 2.3. Месяцы с наибольшими продажами")
    if 'order_date' in df.columns and 'revenue' in df.columns:
        monthly_sales = df.set_index('order_date').resample('ME')['revenue'].sum().reset_index()
        monthly_sales['order_date'] = monthly_sales['order_date'].dt.strftime('%Y-%m')
        monthly_sales = monthly_sales.sort_values(by='revenue', ascending=False)
        
        st.write(monthly_sales.set_index('order_date'))
        st.info("**Вывод:** Периоды пиковой активности покупателей и сезонность.")

    st.markdown("### 2.4. Расчет среднего чека")
    if 'revenue' in df.columns:
        st.metric("Средний чек", f"{df['revenue'].mean():.2f}")
        st.info("**Вывод:** Показывает среднюю сумму одного заказа.")

    st.markdown("### 2.5. Клиенты с наибольшим количеством заказов")
    if 'customer_name' in df.columns:
        st.write(df['customer_name'].value_counts().head(5))
        st.info("**Вывод:** Самые активные покупатели.")

else:
    st.warning("Пожалуйста, загрузите CSV-файл")
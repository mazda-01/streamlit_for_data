import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Скрываем все ссылки на страницы в боковой панели
# Аве, GPT
st.markdown(
    """
    <style>
    /* Скрываем заголовок "Pages" */
    [data-testid="stSidebar"] > div:first-child > div:first-child > h2 {
        display: none;
    }
    
    /* Скрываем список страниц */
    [data-testid="stSidebar"] > div:first-child > div:nth-child(2) {
        display: none;
    }
    
    /* Если нужно — скрываем разделитель */
    [data-testid="stSidebar"] > div:first-child > hr {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

apple = yf.Ticker('AAPL')
hist = apple.history(period='6mo')

st.set_page_config(page_title='Работа с DataFrame')
st.title('Работа с DataFrame - CSV, XLSX')

#data Apple
st.subheader('Принудительный отчет - Apple 😩')
st.write('Данные компании Apple за последние полгода')
st.dataframe(hist, height=230)

info_apple = apple.info

#Графика цен  акций Apple
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=hist.index,
    y=hist.Close,
    mode='lines + markers',
    hovertemplate='<b>Дата</b>: %{x}<br><b>Цена</b>: $%{y:.2f}<extra></extra>'
))

fig.update_layout(
    title={
    'text': '📊Цена акций Apple за последние 6 месяцев',
    'xanchor': 'center',
    'x': 0.5,
    'y': 0.9
    },
    xaxis_title='Дата',
    yaxis_title='Цена ($)',
    template='presentation',
    height=500
)
st.plotly_chart(fig, use_container_width=True)

latest_price = hist['Close'].iloc[-1]
st.metric("Текущая цена", f"${latest_price:.2f}", delta=None)

#Инфа об Apple
st.subheader('Краткая инфа👀')
st.write(f'Название: {info_apple.get('longName')}')
st.write(f'Сайт: {info_apple.get('website')}')
st.write(f'Сектор: {info_apple.get('sector')}')
st.write(f'Рыночная капитализация: {info_apple.get('marketCap')} USD')

#SideBars
csv = hist.to_csv(index=True).encode('utf-8')
st.sidebar.download_button('Скачать DataFrame Apple', csv, file_name='apple.csv')

st.sidebar.title('Навигация 🧭')
st.sidebar.page_link('main.py', label='Главная', icon='🏠')
st.sidebar.page_link('pages/apple.py', label='Apple', icon='🍏')
st.sidebar.page_link('pages/update.py', label='Загрузка и обработка', icon='🗄️')
st.sidebar.page_link('pages/analysis.py', label='Анализ', icon='📊')





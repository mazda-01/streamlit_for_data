import streamlit as st
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

st.title('Работа с DataFrame - CSV, XLSX')

st.subheader('Пример:')

df = pd.read_csv('tips.csv')
df.drop(columns='Unnamed: 0', inplace=True)
st.dataframe(df, height=230)

col1, col2, col3 = st.columns([1, 3, 3])
with col2:
    x = st.radio('Выбери колонку - кого изучать',
                [col for col in df.select_dtypes(include='object').columns])
    st.session_state.x = x
with col3:
    y = st.radio('Выбери колонку - что изучать',
                [col for col in df.select_dtypes(include='number').columns])
    st.session_state.y = y

x = st.session_state.x
y = st.session_state.y

fig = go.Figure(data=go.Pie(labels=df[x], values=df[y]))

fig.update_layout(
    title={
    'text': 'Анализ tips.csv',
    'xanchor': 'center',
    'x': 0.425,
    'y': 0.9
    },
    template='ggplot2',
    height=500
)
st.plotly_chart(fig, use_container_width=True)

#SideBars
csv = df.to_csv(index=True).encode('utf-8')
st.sidebar.download_button('Скачать DataFrame Tips', csv, file_name='tips.csv')

st.sidebar.title('Навигация 🧭')
st.sidebar.page_link('main.py', label='Главная', icon='🏠')
st.sidebar.page_link('pages/apple.py', label='Apple', icon='🍏')
st.sidebar.page_link('pages/update.py', label='Загрузка и обработка', icon='🗄️')
st.sidebar.page_link('pages/analysis.py', label='Анализ', icon='📊')





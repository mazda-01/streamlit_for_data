import streamlit as st
import pandas as pd


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

st.title('📊 Анализ')

choice = st.selectbox('С каким DF будем работать?', ('Загрузить', 'Обработаный'))

if choice == 'Загрузить':
    file = st.file_uploader('', type=['csv', 'xlsx'], help='Поддерживаются форматы .csv и .xlsx')
    st.session_state.file = file
else:
    if 'df' not in st.session_state:
        st.info('❌ Перейди в "Загрузка и обработка" и загрузи файл')
    else:
        df = st.session_state.df
        st.dataframe(df, height=230)

        col1, col2, col3 = st.columns([1, 3, 3])
        with col2:
            x = st.radio('Выбери колонку для X оси', [col for col in df.columns])
            st.session_state.x = x
        with col3:
            y = st.radio('Выбери колонку для Y оси', [col for col in df.columns])
            st.session_state.y = y
        
        try:
            st.subheader('Линейный график')
            df = st.session_state.df
            x = st.session_state.x
            y = st.session_state.y

            st.line_chart(data=df, x=x, y=y, use_container_width=True, height=500)
        except:
            st.info('❌ Выбери другую X или Y колонку')
        
        try:
            st.subheader('Столбчатая диаграмма')
            df = st.session_state.df
            x = st.session_state.x
            y = st.session_state.y

            st.bar_chart(data=df, x=x, y=y, use_container_width=True, height=500)
        except:
            st.info('❌ Выбери другую X или Y колонку')


if 'file' in st.session_state and st.session_state.file is not None:
    file = st.session_state.file
    if file.name.endswith('.csv'):
        df = pd.read_csv(file, encoding='latin1')
        st.session_state.df = df
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
        st.session_state.df = df
    else:
        st.error('Неподдерживаемый файл')
        st.stop()
    df = st.session_state.df
    st.dataframe(df, height=230)

    col1, col2, col3 = st.columns([1, 3, 3])
    with col2:
        x = st.radio('Выбери колонку для X оси', [col for col in df.columns])
        st.session_state.x = x
    with col3:
        y = st.radio('Выбери колонку для Y оси', [col for col in df.columns])
        st.session_state.y = y
    
    try:
        st.subheader('Линейный график')
        df = st.session_state.df
        x = st.session_state.x
        y = st.session_state.y

        st.line_chart(data=df, x=x, y=y, use_container_width=True)
    except:
        st.info('❌ Выбери другую X или Y колонку')
    
    try:
        st.subheader('Столбчатая диаграмма')
        df = st.session_state.df
        x = st.session_state.x
        y = st.session_state.y

        st.bar_chart(data=df, x=x, y=y, use_container_width=True)
    except:
        st.info('❌ Выбери другую X или Y колонку')

#SideBars
st.sidebar.title('Навигация 🧭')
st.sidebar.page_link('main.py', label='Главная', icon='🏠')
st.sidebar.page_link('pages/apple.py', label='Apple', icon='🍏')
st.sidebar.page_link('pages/update.py', label='Загрузка и обработка', icon='🗄️')
st.sidebar.page_link('pages/analysis.py', label='Анализ', icon='📊')




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

st.title('Загрузка и обработка DataFrame')
#Загрузка файла
file = st.file_uploader('', type=['csv', 'xlsx'], help='Поддерживаются форматы .csv и .xlsx')

if file is not None:

    if 'file_name' not in st.session_state or st.session_state.file_name != file.name:
        st.session_state.file_name = file.name
        st.session_state.df = None

    st.subheader('📊 Исходные данные')
    if file.name.endswith('.csv'):
        df = pd.read_csv(file, encoding='latin1')
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        st.error('Неподдерживаемый файл')
        st.stop()

    st.dataframe(df, height=230)

    if st.session_state.df is None:
        st.session_state.df = df

    st.subheader('Работа с пропусками')
    miss = df.isna().sum()


    if miss.sum() == 0:
        st.info('Пропуски отсутствуют!')
    else:
        st.dataframe(miss[miss > 0])
        st.write(f'Найдено пропусков: {miss.sum()}')

        col1, col2 = st.columns([3, 2])
        with col1:
            if st.button('Удалить колонки - все пропуски'):
                df = st.session_state.df
                missed_col = df.isna().sum().sum()
                
                if missed_col == 0:
                    st.success('❌ Пропусков не осталось!')
                else:    
                    test_col = df.dropna(axis=1, how='all')
                    if len(df.columns) == len(test_col.columns):
                        st.success('❌ Такие колонки отсутствуют!')
                    else:
                        df.dropna(axis=1, how='all', inplace=True)    
                        st.success('✅ Колонки успешно удалены!')
                        
                        st.session_state.df = df
            
            if st.button('Удалить строки с пропусками'):
                df = st.session_state.df
                miss = df.isna().sum().sum()
                if miss == 0:
                    st.success('❌ Пропусков не осталось!')
                else:    
                    df.dropna(inplace=True)

                    st.success('✅ Пропуски успешно удалены!')

                    st.session_state.df = df

        with col2:
            if st.button('Заполнить пропуски - mean'):
                df = st.session_state.df
                miss = df.isna().sum().sum()

                cnt = 0
                for col in df.select_dtypes(include='number').columns:
                        if df[col].isnull().sum() > 0:
                            cnt += 1
                            break

                if miss == 0:
                    st.success('❌ Пропусков не осталось!')
                elif cnt == 0:
                    st.success('❌ Числовые колонки с пропусками отсутствуют')
                else:
                    for col in df.select_dtypes(include='number').columns:
                        if df[col].isnull().sum() > 0:
                            mean_val = df[col].mean()
                            df[col].fillna(round(mean_val, 0), inplace=True)
                            st.session_state.df = df

                    st.session_state.df = df
                    st.success('✅ Успешно заменено!')

            if st.button('Заполнить пропуски - mode'):
                df = st.session_state.df
                miss = df.isna().sum().sum()

                cnt = 0
                for col in df.select_dtypes(include='object').columns:
                        if df[col].isnull().sum() > 0:
                            cnt += 1
                            break

                if miss == 0:
                    st.success('❌ Пропусков не осталось!')
                elif cnt == 0:
                    st.success('❌ Категориальные колонки с пропусками отсутствуют')
                else:
                    for col in df.select_dtypes(include='object').columns:
                        if df[col].isnull().sum() > 0:
                            if not df[col].mode().empty:
                                mode_val = df[col].mode()[0]
                            else:
                                mode_val = 'Неизвестно'
                            df[col].fillna(mode_val, inplace=True)
                            st.session_state.df = df

                    st.session_state.df = df
                    st.success('✅ Успешно заменено!')
        st.write('')
        st.write('Проверка и отображение')
        if st.button('Проверить наличие пропусков!'):
                df = st.session_state.df

                miss_info = df.isna().sum().sum()

                if miss_info == 0:
                    st.success('✅ Все пропуски истреблены!')
                    st.dataframe(df, height=230)
                else:
                    st.info(f'Пропусков осталось: {miss_info}')

    st.subheader('Работа с дубликатами')
    df = st.session_state.df
    duplicates = df.duplicated().sum()

    if duplicates == 0:
        st.info('Дубликаты отсутствуют')
    else:
        st.info(f'Дубликатов найдено: {duplicates[duplicates > 0].sum()}')
        
        if st.button('🗑️ Удалить дубликаты'):
            df = st.session_state.df

            df.drop_duplicates(inplace=True)
            st.success('✅ Дубликаты успешно истреблены!')
            st.dataframe(df, height=230)

    df = st.session_state.df
    csv = df.to_csv(index=True).encode('utf-8')
    st.sidebar.download_button('Скачать DataFrame', csv, file_name='data.csv')

else:
   st.info('Загрузи файл, чтобы продолжить')

#SideBars
st.sidebar.title('Навигация 🧭')
st.sidebar.page_link('main.py', label='Главная', icon='🏠')
st.sidebar.page_link('pages/apple.py', label='Apple', icon='🍏')
st.sidebar.page_link('pages/update.py', label='Загрузка и обработка', icon='🗄️')
st.sidebar.page_link('pages/analysis.py', label='Анализ', icon='📊')
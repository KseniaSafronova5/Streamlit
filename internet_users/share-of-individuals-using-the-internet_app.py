import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os 


# Настройка страницы для использования всей доступной ширины
st.set_page_config(layout="wide")

# Заголовок приложения
st.title("Глобальная модель мониторинга использования интернета")

# --- Загрузка данных ---
@st.cache_data
def load_data(filepath):
    # Используем абсолютный путь к файлу на основе расположения текущего скрипта
    script_dir = os.path.dirname(__file__) # Получаем директорию, где лежит этот скрипт
    abs_file_path = os.path.join(script_dir, filepath) # Собираем полный путь
    df = pd.read_csv(abs_file_path) # Читаем по полному пути
    df['Year'] = df['Year'].astype(int)
    return df

# Указываем только имя файла, который лежит рядом с app.py
DATA_FILE = 'share-of-individuals-using-the-internet.csv'
df = load_data(DATA_FILE)

# --- Фильтрация данных по общему диапазону лет (1995-2017) ---
MIN_YEAR = 1995
MAX_YEAR = 2017
df_filtered_range = df[(df['Year'] >= MIN_YEAR) & (df['Year'] <= MAX_YEAR)]


# --- Боковая панель для второй части ---
st.sidebar.header("Country level detail")
# Используем отфильтрованный df_filtered_range для получения списка стран
available_countries = sorted(df_filtered_range['Country'].unique()) 

# Устанавливаем default=[] (пустой список), чтобы пользователь выбирал сам
selected_countries = st.sidebar.multiselect("Select Countries", available_countries, default=[])

submit_button = st.sidebar.button("Submit")

# --- Основной макет для первой части ---

st.header("Internet Usage Dashboard")

# 1. Выпадающий список годов (с 2000 по 2017)
# Обратите внимание, здесь мы все еще используем года с 2000 по 2017 для КАРТЫ и ГИСТОГРАММЫ
available_years_map = sorted([year for year in df_filtered_range['Year'].unique() if 2000 <= year <= 2017])
selected_year = st.selectbox("Год для карты и гистограммы", available_years_map, index=len(available_years_map) - 1)

st.subheader(f"Визуализация данных за {selected_year} год")

# Фильтруем данные по выбранному году
filtered_df_year = df_filtered_range[df_filtered_range['Year'] == selected_year]

# Используем st.columns для создания двух колонок равной ширины
col1, col2 = st.columns(2)

# 2. Карта мира (без легенды и лишнего заголовка)
with col1:
    fig_map = px.choropleth(filtered_df_year, locations="Code",
                            color="Individuals using the Internet (% of population)",
                            hover_name="Country",
                            color_continuous_scale=px.colors.sequential.Plasma,
                            title=f"Использование интернета в {selected_year}")
    
    fig_map.update_layout(coloraxis_showscale=False)

    st.plotly_chart(fig_map, use_container_width=True)

# 3. Гистограмма распределения (без лишнего заголовка)
with col2:
    fig_hist = px.histogram(filtered_df_year, x="Individuals using the Internet (% of population)",
                            nbins=20, title="Распределение использования интернета")
    st.plotly_chart(fig_hist, use_container_width=True)


# --- Вторая часть: Линейный график по стране/странам (обновляется при нажатии кнопки) ---

if submit_button:
    if selected_countries:
        st.subheader(f"Динамика использования интернета в выбранных странах c {MIN_YEAR} по {MAX_YEAR} гг.")
        
        # Фильтруем данные для выбранных стран из df_filtered_range (1995-2017)
        countries_df = df_filtered_range[df_filtered_range['Country'].isin(selected_countries)]
        
        if not countries_df.empty:
            fig_line = px.line(countries_df, x="Year", y="Individuals using the Internet (% of population)",
                               color='Country',
                               title=f"Динамика использования интернета в {', '.join(selected_countries)}")
            st.plotly_chart(fig_line)
        else:
            st.warning("Данные для выбранных стран отсутствуют в выбранном диапазоне лет.")
    else:
        st.warning("Пожалуйста, выберите хотя бы одну страну.")

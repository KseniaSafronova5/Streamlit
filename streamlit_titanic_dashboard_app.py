# my first app on github
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Название дашборда
st.title("Titanic Dashboard")

# --- 1. Загрузка и подготовка данных ---
# Замените 'titanic.csv' на реальный путь к вашему файлу данных,
# или используйте загрузку из seaborn, как в примере ниже
try:
    df = sns.load_dataset('titanic')
except:
    st.error("Ошибка загрузки данных Titanic. Убедитесь, что файл 'titanic.csv' существует или используйте подключение к Kaggle API.")
    st.stop()

# Замена пропущенных значений в Embarked для корректной работы фильтра
df['embark_town'] = df['embark_town'].fillna('Unknown')
# Удаляем строки с пропущенными ценами билетов, если нужно
df.dropna(subset=['fare'], inplace=True) 

# --- 2. Фильтры (Выпадающие списки) ---
# Получаем уникальные значения для фильтров
ports = sorted(df['embark_town'].unique())
genders = sorted(df['sex'].unique())

# Добавляем опцию "Ничего не выбрано"
ports.insert(0, "Ничего не выбрано")
genders.insert(0, "Ничего не выбрано")

# Размещаем фильтры в две колонки
col1, col2 = st.columns(2)
with col1:
    selected_port = st.selectbox("Select a port", ports)
with col2:
    selected_gender = st.selectbox("Select a gender", genders)

# Фильтруем данные в зависимости от выбора пользователя
filtered_df = df.copy()
if selected_port != "Ничего не выбрано":
    filtered_df = filtered_df[filtered_df['embark_town'] == selected_port]
if selected_gender != "Ничего не выбрано":
    filtered_df = filtered_df[filtered_df['sex'] == selected_gender]

# Проверка, остались ли данные после фильтрации
if filtered_df.empty:
    st.warning("Нет данных, соответствующих выбранным фильтрам.")
else:
        # --- 3. Визуализация графиков ---

    st.header("Распределения данных")

    # Создаем две колонки для размещения графиков рядом
    col3, col4 = st.columns(2)

    # Гистограмма Распределения возраста (Distribution of Age)
    with col3:
        st.subheader("Распределение возраста")
        fig_age = px.histogram(filtered_df, x="age", color="survived",
                               nbins=20, title="Возраст по статусу выживания")
        st.plotly_chart(fig_age, use_container_width=True)

    # Круговая диаграмма Passenger ID и Survived (Count of passengers that survived)
    with col4:
        st.subheader("Доля выживших")
        survival_counts = filtered_df['survived'].value_counts().reset_index()
        survival_counts.columns = ['Survived', 'Count']
        # Меняем 0/1 на понятные метки
        survival_counts['Survived_Label'] = survival_counts['Survived'].map({0: 'Не выжил', 1: 'Выжил'})
        
        fig_survived = px.pie(survival_counts, values='Count', names='Survived_Label',
                              title='Распределение выживших')
        st.plotly_chart(fig_survived, use_container_width=True)
    
    # Боксплот остается внизу, как было
    st.subheader("Распределение стоимости билета в зависимости от выживаемости")
    fig_fare = px.box(filtered_df, x='survived', y='fare', 
                      title='Стоимость билета по статусу выживания (0: Не выжил, 1: Выжил)')
    st.plotly_chart(fig_fare, use_container_width=True)



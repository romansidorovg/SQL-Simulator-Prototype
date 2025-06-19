import pandas as pd
import streamlit as st
import psycopg2
from psycopg2 import sql

# Функция подключения к базе данных PostgreSQL
def get_connection():
    return psycopg2.connect(
        host="158.160.86.138",
        port="5432",
        database="user_db",
        user="admin",
        password="lfosdf9282fjkfFjs"
    )

# Заголовок и ввод
st.title("🧠 SQL-тренажёр: запросы к таблице users")
st.write("Введите SQL-запрос, чтобы получить уникальных пользователей из России.")

# Поле ввода SQL-запроса
user_query = st.text_area("Введите SQL-запрос:", height=150, placeholder="Пример: SELECT * FROM users")

# Эталонный SQL-запрос
expected_query = """
SELECT DISTINCT user_id
FROM users
WHERE country = 'Russia'
ORDER BY user_id
"""

# Только если есть непустой запрос от пользователя
if user_query.strip():
    try:
        # Подключаемся один раз и используем соединение для обоих запросов
        with get_connection() as conn:
            expected_result = pd.read_sql_query(expected_query, conn)
            user_result = pd.read_sql_query(user_query, conn)

        # Сортируем и сравниваем
        expected_result = expected_result.sort_values(by="user_id").reset_index(drop=True)
        user_result = user_result.sort_values(by="user_id").reset_index(drop=True)

        if user_result.equals(expected_result):
            st.success("✅ Всё верно! Результат совпадает с ожидаемым.")
            st.dataframe(user_result)
        else:
            st.error("❌ Результат неверный. Проверь условия запроса.")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Ожидалось:**")
                st.dataframe(expected_result)
            with col2:
                st.markdown("**Получено:**")
                st.dataframe(user_result)

    except Exception as e:
        st.error("❌ Ошибка при выполнении запроса:")
        st.code(str(e))
else:
    st.info("Введите SQL-запрос выше для проверки.")

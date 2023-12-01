import sqlite3
import os
import pandas as pd


def table_info(table_name, db_path_):
    conn_ = sqlite3.connect(str(db_path_))
    # Создание курсора для выполнения SQL-запросов
    cur_ = conn_.cursor()
    columns_query_ = f"PRAGMA table_info({str(table_name)})"
    # Выполнение запроса
    cur_.execute(columns_query_)
    # Получение результатов имен столбцов
    columns_ = cur_.fetchall()
    column_list_ = []
    if columns_:
        # print(f"Имена столбцов для таблицы {table_name}:")
        for column_ in columns_:
            # print(column_[1])  # Имя столбца находится во второй позиции результата запроса
            column_list_.append(column_[1])
    else:
        # print(f"Таблица {table_name} не найдена")
        column_list_.append(f'Таблица {table_name} не найдена')
    cur_.close()
    conn_.close()
    return column_list_


def user_info(user_id_, user_id_type_, columns_list_, db_path_):
    search_param_ = {'1':'ID',
                     '2':'Worker',
                     '3':'PhoneNumber',
                     '4':'WorkMail',
                     '5':''
                     }
    search_column_ = search_param_[f'{str(user_id_type_)}']
    print(search_column_)
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    # Создание курсора для выполнения SQL-запросов
    cur_ = conn_.cursor()
    columns_str_ = ', '.join(columns_list_)
    print(columns_str_, '--', user_id_)
    select_query_ = f"SELECT {columns_str_} FROM users WHERE {search_column_} = '{user_id_}'"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    print(rows_)
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            print(row_as_dict_)  # Вывод словаря для каждой строки
    else:
        print("Данные не найдены")


if __name__ == '__main__':

    # Подключение к базе данных SQLite
    conn = sqlite3.connect(f'{os.getcwd()}/data/DSA.db')  # Замените на имя вашей базы данных SQLite

    # Создание курсора для выполнения SQL-запросов
    cur = conn.cursor()

    # SQL-запрос для выбора первых 10 строк из таблицы
    select_query = "SELECT * FROM users LIMIT 10"  # Замените на имя вашей таблицы

    # Выполнение запроса
    cur.execute(select_query)

    # Получение результатов запроса и вывод на экран
    rows = cur.fetchall()
    for row in rows:
        print(row)

    # Закрытие курсора и соединения
    bd_path = f'{os.getcwd()}/data/DSA.db'
    print(bd_path)
    cur.close()
    conn.close()
    column_list = table_info('users', bd_path)
    print(column_list)
    columns = ['Worker', 'Kabinet', 'PhoneNumber', 'WorkMail']
    worker = 'Габитов Динар Шаукатович'
    user_info(worker, 2, columns, bd_path)

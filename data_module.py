import sqlite3
import os
import re
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
    search_param_ = {'1': 'ID',
                     '2': 'Worker',
                     '3': 'PhoneNumber',
                     '4': 'WorkMail',
                     '5': 'Kabinet',
                     '6': 'TG_id',
                     '7': 'SEDO_id'
                     }
    search_column_ = search_param_[f'{str(user_id_type_)}']
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    columns_str_ = ', '.join(columns_list_)
    print(user_id_)
    select_query_ = f"SELECT {columns_str_} FROM users WHERE {search_column_} LIKE '%{user_id_}%'"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    result_ = []
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            result_.append(row_as_dict_)
    else:
        result_.append("Данные не найдены")
    return result_


def search_cat(search_):
    type_ = ''
    pattern_work_number_ = r'\d\d-\d\d\d'
    pattern_email_ = r'\w+@\w+.ru'
    pattern_cabinet_ = r'\d+[.]\d+'
    pattern_tg_id_ = r'tg_id_::\d+'
    pattern_sedo_id_ = r'sedo_id::\d+'
    pattern_id_ = r'users_id::\d+'
    if re.search(pattern_work_number_, search_):
        type_ = '3'
    elif re.search(pattern_email_, search_):
        type_ = '4'
    elif re.search(pattern_cabinet_, search_):
        type_ = '5'
    elif re.search(pattern_tg_id_, search_):
        type_ = '6'
    elif re.search(pattern_sedo_id_, search_):
        type_ = '7'
    elif re.search(pattern_id_, search_):
        type_ = '1'
    else:
        type_ = '2'
    return type_


def update_table(table_name_, db_path_, columns_, values_, search_par_, search_):
    search_param_ = {'1': 'ID',
                     '2': 'Worker',
                     '3': 'PhoneNumber',
                     '4': 'WorkMail',
                     '5': 'Kabinet',
                     '6': 'TG_id',
                     '7': 'SEDO_id'
                     }
    conn_ = sqlite3.connect(str(db_path_))
    # Создание курсора для выполнения SQL-запросов
    cur_ = conn_.cursor()
    set_param_ = ''
    i = 0
    for column_ in columns_:
        set_param_ = str(column_) + ' = ' + "'"+str(values_[i])+"'"
        if column_ == columns_[-1]:
            set_param_ = set_param_ + ' '
        else:
            set_param_ = set_param_ + ', '
    print(set_param_)
    columns_query_ = f"UPDATE {str(table_name_)} SET {set_param_}WHERE {search_param_[search_par_]} = {search_}"
    print(columns_query_)
    # Выполнение запроса
    cur_.execute(columns_query_)
    conn_.commit()
    cur_.close()
    conn_.close()
    # Получение результатов имен столбцов
    return 'Update complete'


if __name__ == '__main__':


    bd_path = f'{os.getcwd()}/data/DSA.db'
    print(table_info('users', bd_path))
    # # print(bd_path)
    # cur.close()
    # conn.close()
    column_list = table_info('users', bd_path)
    # print(column_list)
    columns = ['ID', 'Worker', 'Kabinet', 'PhoneNumber', 'WorkMail', 'MainMobilePhone', 'TG_id']
    worker = 'users_id::546'
    search_type = search_cat(worker)
    if '::' in worker:
        worker = worker.split('::')[1]
    print(user_info(worker, search_type, columns, bd_path))
    # update_table('users', bd_path, ['TG_id'], ['309025156'], search_type, worker)

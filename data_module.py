import sqlite3
import os
import re
import pandas as pd
import logging
import text
from datetime import  datetime
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a", format="%(asctime)s %(levelname)s %(message)s")


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


def update_table(table_name_, columns_, values_, search_par_, search_, sender_id_):
    if check_admin(sender_id_) == 1:
        db_path_ = f'{os.getcwd()}/data/DSA.db'
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
        set_param_ = ''
        for column_ in columns_:
            set_param_ = set_param_ + str(column_) + ' = ' + "'"+str(values_[i])+"'"
            if column_ == columns_[-1]:
                set_param_ = set_param_ + ' '
            else:
                set_param_ = set_param_ + ', '
            i = i+1
        columns_query_ = f"UPDATE {str(table_name_)} SET {set_param_}WHERE {search_param_[search_par_]} = '{search_}'"
        print(columns_query_)
        # Выполнение запроса
        cur_.execute(columns_query_)
        conn_.commit()
        cur_.close()
        conn_.close()
        # Получение результатов имен столбцов
        return 'Update complete'
    else:
        return 'Извините, у вас нет прав на это действие'


def whoami(tg_id_):
    bd_path_ = f'{os.getcwd()}/data/DSA.db'
    columns_ = ['ID', 'Worker', 'Kabinet', 'PhoneNumber', 'WorkMail', 'MainMobilePhone', 'TG_id', 'SEDO_id', 'notification_time']
    worker_ = f'tg_id_::{tg_id_}'
    search_type_ = search_cat(worker_)
    if '::' in worker_:
        worker_ = int(worker_.split('::')[1])
        print(worker_)
    a = user_info(worker_, search_type_, columns_, bd_path_)
    return a


def search(search_, tg_id_):
    logging.info(f'{search_sender(tg_id_)} ищет {str(search_)}')
    bd_path_ = f'{os.getcwd()}/data/DSA.db'
    columns_ = ['ID', 'Worker', 'Kabinet', 'PhoneNumber', 'WorkMail', 'MainMobilePhone', 'TG_id',
                'OrganizationDevelopment1Calc', 'WorkersTitleCalc', 'UPRAVLENIE1Calc', 'TG_chat_id']
    worker_ = f'tg_id_::{tg_id_}'
    if '::' in worker_:
        worker_ = int(worker_.split('::')[1])
        print(worker_)
    search_type_ = search_cat(search_)
    a = user_info(search_, search_type_, columns_, bd_path_)
    if a[0] == 'Данные не найдены':
        reply = 'Данные не найдены'
    else:
        reply = text.whoami.format(fio=a[0]['Worker'], phone=a[0]['PhoneNumber'], email=a[0]['WorkMail'],
                                   cabinet=a[0]['Kabinet'], Worker_type=a[0]['WorkersTitleCalc'],
                                   otdel=a[0]['OrganizationDevelopment1Calc'], upravlenie=a[0]['UPRAVLENIE1Calc'], chat_id=a[0]['TG_chat_id'])
    return reply


def chat_checker(tg_id_, chat_id_):
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    columns_list_ = ['ID', 'Worker', 'TG_id', 'TG_chat_id']
    columns_str_ = ', '.join(columns_list_)
    print(tg_id_)
    user_id_ = int(tg_id_)
    select_query_ = f"SELECT {columns_str_} FROM users WHERE TG_id = '{user_id_}'"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    result_ = []
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            result_.append(row_as_dict_)
    else:
        result_.append("Данные не найдены")
    if not result_[0] == "Данные не найдены":
        columns_query_ = f"UPDATE users SET TG_chat_id = {chat_id_} WHERE TG_id = {int(tg_id_)}"
        # Выполнение запроса
        cur_.execute(columns_query_)
        conn_.commit()
        cur_.close()
        conn_.close()
    return


def search_sender(tg_id_):
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    select_query_ = f"SELECT Worker, TG_id FROM users WHERE TG_id = '{int(tg_id_)}'"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    result_ = []
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            result_.append(row_as_dict_)
            print(result_[0]['Worker'])
            return result_[0]['Worker']
    else:
        result_.append("Данные не найдены")
        print(result_[0])
        return result_[0]


def check_admin(tg_id_):
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    select_query_ = f"SELECT Worker, TG_id, admin_int FROM users WHERE TG_id = '{int(tg_id_)}' AND admin_int = '1'"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    if rows_:
        return 1
    else:
        return 0


def notification_search(time_):
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    # select_query_ = f"SELECT TG_id, notification_type, notification_status, date, time, text FROM notifications WHERE notification_status > 0"
    select_query_ = f"SELECT TG_id, TG_chat_id, Worker, SEDO_id, notification_time FROM users WHERE TG_chat_id > 0"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    answer_0_ = []
    answer_1_ = []
    result_ = []
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            result_.append(row_as_dict_)
        print(result_)
        for item_ in result_:
            if time_ in item_['notification_time']:
                answer_0_.append(item_)
                # if item_['notification_type'] == 1:
                #     answer_1_.append(item_)
                # if item_['notification_type'] == 0:
                #     answer_0_.append(item_)
    return answer_0_, answer_1_


def foo(tg_id_):
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    select_query_ = f"SELECT Worker, TG_id, admin_int FROM users WHERE TG_id = '{int(tg_id_)}'"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    result_ = []
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            result_.append(row_as_dict_)
            print(result_[0]['Worker'])
            return result_[0]['Worker']
    else:
        return 0


if __name__ == '__main__':
    time_start = datetime.now()
    a, b = notification_search('17:00')
    print(len(a))
    print(datetime.now() - time_start)
    # bd_path = f'{os.getcwd()}/data/DSA.db'
    # print(table_info('users', bd_path))


    # # print(bd_path)
    # cur.close()
    # conn.close()
    # column_list = table_info('users', bd_path)
    # print(column_list)
    # columns = ['ID', 'Worker', 'Kabinet', 'PhoneNumber', 'WorkMail', 'MainMobilePhone', 'TG_id', 'admin_int', 'notification_time']
    # worker = 'Арсеньев'
    # search_type = search_cat(worker)
    # if '::' in worker:
    #     worker = worker.split('::')[1]
    # a = user_info(worker, search_type, columns, bd_path)
    # for item in a:
    #     print(item)
    #
    # df = pd.read_excel('/Users/viktor/Downloads/сотрудники.xlsx', sheet_name='Лист1')
    # df = df[['ID','СЭДО','Телеграм']].fillna(-1)
    # list_id = df['ID'].to_list()



    # list_sedo = df['СЭДО'].to_list()
    #
    #
    #
    # list_tg = df['Телеграм'].to_list()
    # print(list_tg)
    # conn = sqlite3.connect(str(bd_path))
    # # Создание курсора для выполнения SQL-запросов
    # cur = conn.cursor()
    # columns_query = f"UPDATE users SET TG_chat_id = -1 WHERE TG_chat_id IS NULL"
    # columns_query = f"ALTER TABLE users ADD notification_time TEXT DEFAULT '';"
    # # Выполнение запроса
    # cur.execute(columns_query)
    # conn.commit()
    # cur.close()
    # conn.close()



    # for i in range(len(list_id)):
    #     worker = f'users_id::{list_id[i]}'
    #     search_type = search_cat(worker)
    #     if '::' in worker:
    #         worker = worker.split('::')[1]
    #     update_table('users', ['TG_id', 'SEDO_id'], [str(list_tg[i]), str(list_sedo[i])], search_type, worker)
    # list_id.append(390)
    # for id in list_id:
    #     worker = f'users_id::{id}'
    #     search_type = search_cat(worker)
    #     if '::' in worker:
    #         worker = worker.split('::')[1]
    #     a = user_info(worker, search_type, columns, bd_path)
    # print(list_tg)
    # update_table('users', bd_path, ['TG_id'], ['309025156'], search_type, worker)

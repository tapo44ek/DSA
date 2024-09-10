import sqlite3
import os
import re
import time
import numpy as np
import pandas as pd
import logging
import text
from datetime import datetime
logging.basicConfig(level=logging.INFO, filename="py_log.log",
                    filemode="a", format="%(asctime)s %(levelname)s %(message)s")


def user_list():
    bd_path_ = f'{os.getcwd()}/data/DSA.db'
    search_column_ = 'WorkersTitle'
    conn_ = sqlite3.connect(str(bd_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    select_query_ = f"SELECT TG_id FROM users WHERE TG_chat_id > 0;"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    result_ = []
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            result_.append(row_as_dict_)
            # print(result_)
    else:
        result_.append({'TG_id': "Данные не найдены"})
    return result_


def get_sogl_info(tg_id_):
    bd_path_ = f'{os.getcwd()}/data/DSA.db'
    search_column_ = 'WorkersTitle'
    conn_ = sqlite3.connect(str(bd_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    select_query_ = f"SELECT TG_id, SEDO_id, Worker FROM users WHERE TG_id = {tg_id_}"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    result_ = []
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            result_.append(row_as_dict_)
            # print(result_)
    else:
        result_.append({'WorkersTitle': "Данные не найдены"})
    return result_[0]


def get_title(tg_id_):
    bd_path_ = f'{os.getcwd()}/data/DSA.db'
    search_column_ = 'WorkersTitle'
    conn_ = sqlite3.connect(str(bd_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    select_query_ = f"SELECT WorkersTitle FROM users WHERE TG_id = {tg_id_}"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    result_ = []
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            result_.append(row_as_dict_)
            # print(result_)
    else:
        result_.append({'WorkersTitle': "Данные не найдены"})
    return result_[0]['WorkersTitle']


def get_email(tg_id_):
    bd_path_ = f'{os.getcwd()}/data/DSA.db'
    search_column_ = 'TG_id'
    conn_ = sqlite3.connect(str(bd_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    select_query_ = f"SELECT WorkMail FROM users WHERE TG_id = '{tg_id_}'"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    result_ = []
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            result_.append(row_as_dict_)
            # print(result_)
    else:
        result_.append("Данные не найдены")
    return result_[0]['WorkMail']


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


def reg_rg(sender_id_):
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
    # set_param_ = ''
    # i = 0
    # set_param_ = ''
    # for column_ in columns_:
    #     set_param_ = set_param_ + str(column_) + ' = ' + "'"+str(values_[i])+"'"
    #     if column_ == columns_[-1]:
    #         set_param_ = set_param_ + ' '
    #     else:
    #         set_param_ = set_param_ + ', '
    #     i = i+1
    columns_query_ = f"UPDATE users SET TG_id = {sender_id_}, TG_chat_id = {sender_id_} WHERE Worker LIKE '%Биктимиров%'"
    print(columns_query_)
    # Выполнение запроса
    cur_.execute(columns_query_)
    conn_.commit()
    cur_.close()
    conn_.close()
    # Получение результатов имен столбцов
    return 'Update complete'



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
    columns_ = ['ID', 'Worker', 'Kabinet', 'PhoneNumber', 'WorkMail',
                'TG_id', 'WorkersTitle', 'WorkPlace_id', 'TG_chat_id']
    worker_ = f'tg_id_::{tg_id_}'
    if '::' in worker_:
        worker_ = int(worker_.split('::')[1])
        print(worker_)
    search_type_ = search_cat(search_)
    a = user_info(search_, search_type_, columns_, bd_path_)
    if a[0] == 'Данные не найдены':
        reply = 'Данные не найдены'
    else:
        work_place_id = a[0]['WorkPlace_id']
        conn_ = sqlite3.connect(str(bd_path_))
        conn_.row_factory = sqlite3.Row
        cur_ = conn_.cursor()
        select_query_ = f"SELECT * FROM departments WHERE ID = {a[0]['WorkPlace_id']}"
        cur_.execute(select_query_)
        rows_ = cur_.fetchall()
        result_ = []
        if rows_:
            for row_ in rows_:
                row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
                result_.append(row_as_dict_)
        else:
            result_.append({'Otdel':"Данные не найдены", 'Upravlenie':'Данные не найдены'})
        print(result_)
        reply = text.whoami.format(fio=a[0]['Worker'], phone=a[0]['PhoneNumber'], email=a[0]['WorkMail'],
                                   cabinet=a[0]['Kabinet'], Worker_type=a[0]['WorkersTitle'],
                                   otdel=result_[0]['Otdel'], upravlenie=result_[0]['Upravlenie'])
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
    select_query_ = f"SELECT Worker, TG_id, admin_int FROM users WHERE TG_id = '{int(tg_id_)}'"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    if rows_:
        return rows_[0][2]
    else:
        return 0


def set_dnsid(dnsid_):
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    columns_query_ = f"UPDATE dnsid SET status = 0 WHERE dnsid = '{dnsid_}'"
    # print(columns_query_)
    # Выполнение запроса
    cur_.execute(columns_query_)
    conn_.commit()
    cur_.close()
    conn_.close()
    return


def get_report(report):
    #SELECT column FROM table ORDER BY RANDOM() LIMIT 1
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    # select_query_ = f"SELECT TG_id, notification_type, notification_status, date, time, text FROM notifications WHERE notification_status > 0"
    select_query_ = f"SELECT tg_id FROM reports WHERE report_name = '{report}' ORDER BY RANDOM() LIMIT 1"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            tg_id_ = row_as_dict_['tg_id']
            columns_query_ = f"UPDATE reports SET tg_id = 0 WHERE tg_id = {row_as_dict_['tg_id']}"
            # print(columns_query_)
            # Выполнение запроса
            cur_.execute(columns_query_)
            conn_.commit()
            cur_.close()
            conn_.close()

        return tg_id_
    else:
        return 'error'


def set_report(report, tg_id_):
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    columns_query_ = f"UPDATE reports SET tg_id = {tg_id_} WHERE report_name = '{report}'"
    # print(columns_query_)
    # Выполнение запроса
    cur_.execute(columns_query_)
    conn_.commit()
    cur_.close()
    conn_.close()
    return


def get_dnsid():
    #SELECT column FROM table ORDER BY RANDOM() LIMIT 1
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    # select_query_ = f"SELECT TG_id, notification_type, notification_status, date, time, text FROM notifications WHERE notification_status > 0"
    select_query_ = f"SELECT dnsid, status FROM dnsid WHERE status = 0 ORDER BY RANDOM() LIMIT 1"
    cur_.execute(select_query_)
    rows_ = cur_.fetchall()
    if rows_:
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            dnsid_ = row_as_dict_['dnsid']
            columns_query_ = f"UPDATE dnsid SET status = 1 WHERE dnsid = '{row_as_dict_['dnsid']}'"
            # print(columns_query_)
            # Выполнение запроса
            cur_.execute(columns_query_)
            conn_.commit()
            cur_.close()
            conn_.close()

        return dnsid_
    else:
        return 'error'


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
        print(rows_)
        for row_ in rows_:
            row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
            result_.append(row_as_dict_)
        print(result_)
        for item_ in result_:
            print(item_)
            if item_['notification_time'] is not None:
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


def get_notification(tg_id_):
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    columns_query_ = f"SELECT notification_time FROM users WHERE  tg_id = '{tg_id_}'"
    # print(columns_query_)
    # Выполнение запроса
    cur_.execute(columns_query_)
    rows_ = cur_.fetchall()
    result_ = []
    for row_ in rows_:
        row_as_dict_ = dict(row_)  # Преобразование объекта sqlite3.Row в словарь
        result_.append(row_as_dict_)
    cur_.close()
    conn_.close()
    try:
        rez = result_[0]['notification_time']
    except:
        rez = 'Данные отсутствуют'
    return rez


def set_notification(tg_id_, notification_):
    db_path_ = f'{os.getcwd()}/data/DSA.db'
    conn_ = sqlite3.connect(str(db_path_))
    conn_.row_factory = sqlite3.Row
    cur_ = conn_.cursor()
    columns_query_ = f"UPDATE users SET notification_time = '{notification_}' WHERE tg_id = '{tg_id_}'"
    # print(columns_query_)
    # Выполнение запроса
    cur_.execute(columns_query_)
    conn_.commit()
    cur_.close()
    conn_.close()
    return 'Данные обновлены'


if __name__ == '__main__':
    a=1
    # df = pd.read_excel('/Users/viktor/Downloads/Пользователи.xlsx')
    # df = df.replace({np.nan: None})
    #
    # # Convert DataFrame rows into a list of tuples for bulk insert
    # args = list(df.itertuples(index=False, name=None))
    # # Prepare the arguments string for the SQL query
    # try:
    #     # Prepare the arguments string for the SQL query
    #     args_str = ",".join(
    #         "({})".format(
    #             ", ".join(
    #                 "'{}'".format(x.replace("'", "''")) if isinstance(x, str) else "NULL" if x is None else str(x)
    #                 for x in arg
    #             )
    #         )
    #         for arg in args
    #     )
    # except Exception as e:
    #     print(e)
    # db_path_ = f'{os.getcwd()}/data/DSA.db'
    # conn_ = sqlite3.connect(str(db_path_))
    # conn_.row_factory = sqlite3.Row
    # cur_ = conn_.cursor()
    # columns_query_ = f"INSERT INTO users (ID, Worker, WorkPlace_id, WorkersTitle, PhoneNumber, WorkMail, Kabinet, SEDO_id, TG_id, TG_chat_id, admin_int, notification_time) VALUES {args_str}"
    # # print(columns_query_)
    # # Выполнение запроса
    # cur_.execute(columns_query_)
    # conn_.commit()
    # cur_.close()
    # conn_.close()


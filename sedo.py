# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 08:35:31 2023

@author: ArsenevVD
"""
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Process, Queue
from datetime import datetime, timedelta
from handlers import bot
from aiogram.types import Message, FSInputFile
import json
import asyncio
import warnings
import SMTPmail
import config
import sogl_html
import data_module
import re


def sogl_report(FIO, EXECUTOR_ID):
    DNSID = data_module.get_dnsid() #data_module.get_dnsid()  ##wMsWJe-80daXYVWU4d8u_FA  ##w3YG8nxy3qvMCbxDc5lUM5Q
    DNSID1 = DNSID
    warnings.filterwarnings('ignore')
    ds = datetime.now()
    print(ds)
    year = datetime.now().year
    #print(type(year))
    date_now = datetime.strftime(datetime.now(), '%d.%m.%Y')
    url_auth = 'https://mosedo.mos.ru/auth.php?group_id=21'

    with open(f'{os.getcwd()}/settings.json') as f:
        settings = json.load(f)
        token = settings['token2']
        SEDOlog = settings['SEDOlog']
        SEDOpass = settings['SEDOpass']
        #print(SEDOpass)
        PCuser = settings['PCuser']
        UserID = settings['UserID']

    s = requests.Session()

    data = {"DNSID": DNSID,
            "group_id": "21",
            "login": SEDOlog,  # %C0%F0%F1%E5%ED%FC%E5%E2+%C2.%C4.
            "user_id": "80742170",  ##80742170 Арсеньев ##78264321 Габитов
            "password": SEDOpass,
            "token": "",
            "x": "1"}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Connection': 'keep-alive', }

    data_DS = {
        'check_all_projects': 'on',
        'project_type_1': '1',
        'project_type_3': '1',
        'project_type_13': '1',
        'project_type_4': '1',
        'project_type_5': '1',
        'has_period': '1',
        'year_from': f'{str(year-1)}',
        'year_to': f'{str(year)}',
        'order_by': 'default',
        'required_text': '',
        'num': '',
        'rdate_f': '',
        'org_name': '%C4%C3%C8%E3%CC',
        'org': '21',
        'rdate_t': '',
        'reg_user': '',
        'reg_user_id': '',
        'recipient': '',
        'recipient_id': '',
        'recipient_group': '',
        'recipient_group_id': '',
        'in_number': '',
        'bound_number': '',
        'contract_bound_number': '',
        'recipient_org_id': '',
        'cl_out_num': '',
        'cl_out_date_f': '',
        'cl_out_date_t': '',
        'cl_sign': '',
        'cl_sign_id': '',
        'cl_sign_group': '',
        'cl_sign_group_id': '',
        'cl_executor': '',
        'cl_executor_id': '',
        'cl_executor_group': '',
        'cl_executor_group_id': '',
        'cl_text': '',
        'out_number': '',
        'out_date_f': '',
        'out_reg_user': '',
        'out_reg_user_id': '',
        'out_date_t': '',
        'author': '',
        'author_id': '',
        'author_group': '',
        'author_group_id': '',
        'prepared_by': '',
        'prepared_by_id': '',
        'prepared_by_org_id': '',
        'curator': '',
        'curator_id': '',
        'short_content': '',
        'document_kind': '0',
        'delivery_type': '',
        'document_special_kind': '0',
        'external_id': '',
        'has_manual_sign': '0',
        'is_hand_shipping': '0',
        'sign_type': '0',
        'is_dsp': '0',
        'is_control': '0',
        'is_urgent': '0',
        'creator': '',
        'creator_id': '',
        'memo': '',
        'send_date_f': '',
        'send_date_t': '',
        'info': '',
        'info_author': '',
        'info_author_id': '',
        'info_date_f': '',
        'info_date_t': '',
        'og_file_number': '0',
        'rec_vdelo': '0',
        'vdelo_date_f': '',
        'vdelo_date_t': '',
        'vdelo_prepared': '',
        'vdelo_prepared_id': '',
        'vdelo_signed': '',
        'vdelo_signed_id': '',
        'vdelo_text': '',
        'res_type': '0',
        'res_urgency': '0',
        'resolution_num': '',
        'r_rdate_f': '',
        'resolution_creator': '',
        'resolution_creator_id': '',
        'r_rdate_t': '',
        'resolution_author': '',
        'resolution_author_id': '',
        'resolution_author_group': '',
        'resolution_author_group_id': '',
        'resolution_author_org_id': '',
        'r_special_control': '0',
        'resolution_behalf': '',
        'resolution_behalf_id': '',
        'resolution_acting_author': '',
        'resolution_acting_author_id': '',
        'resolution_to': '',
        'resolution_to_id': '',
        'resolution_to_group': '',
        'resolution_to_group_id': '',
        'resolution_to_org_id': '',
        'res_project_letter': '0',
        'res_curator': '',
        'res_curator_id': '',
        'r_control': '0',
        'r_control_f': '',
        'r_control_t': '',
        'r_otv': '0',
        'r_dback': '0',
        'resolution_text': '',
        'r_ef_reason_category_id': '0',
        'r_ef_reason_id': '0',
        'r_is_signed': '0',
        'r_plus': '0',
        'r_another_control': '0',
        'r_oncontrol': '0',
        'r_oncontrol_f': '',
        'r_oncontrol_t': '',
        'unset_control': '0',
        'unset_control_f': '',
        'unset_control_t': '',
        're_date_f': '',
        're_date_t': '',
        're_author': '',
        're_author_id': '',
        're_author_group': '',
        're_author_group_id': '',
        're_acting_author': '',
        're_acting_author_id': '',
        're_is_interim': '-1',
        're_text': '',
        'docs_in_execution': '0',
        're_doc_org_id': '',
        'csdr_initiator': '',
        'csdr_initiator_id': '',
        'csdr_initiator_group': '',
        'csdr_initiator_group_id': '',
        'csdr_start': '0',
        'csdr_start_date_f': '',
        'csdr_start_date_t': '',
        'csdr_stop': '2',
        'csdr_current_version_only': '1',
        'and[csdr][0]': '0',
        'participant_name_0': FIO,
        'participant_name_0_id': EXECUTOR_ID,
        'participant_group_0': '%C4%E5%EF%E0%F0%F2%E0%EC%E5%ED%F2+%E3%EE%F0%EE%E4%F1%EA%EE%E3%EE+%E8%EC%F3%F9%E5%F1%F2%E2%E0+%E3%EE%F0%EE%E4%E0+%CC%EE%F1%EA%E2%FB',
        'participant_group_0_id': '21',
        'csdr_has_deadline_0': '0',
        'csdr_status_0': '2',
        'csdr_init_date_0_f': '',
        'csdr_init_date_0_t': ''
    }

    r = s.post(url_auth, data=data, headers=headers, allow_redirects=False)
    data_module.set_dnsid(DNSID)
    DNSID = r.headers['location'].split('DNSID=')[1]
    print(r.headers)
    print(r.cookies)
    # auth_token = r.cookies.get_dict()['auth_token_s']
    # headers2 = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    #     'Connection': 'keep-alive',
    #     'Sec-Fetch-User': '?1',
    #     'Sec-Fetch-Dest': 'document',
    #     'Cookie': f'auth_token={auth_token};'
    # }
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Connection': 'keep-alive',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document'
    }
    url_sogl = f'https://mosedo.mos.ru/document_search.php?new=0&DNSID={DNSID}'
    print(r)
    s.cookies
    r2 = s.post(url_sogl, data=data_DS, headers=headers2)
    print(r2.text)
    with open("sogl1.html", "w") as file:
        file.write(r2.text)

    first_soup = BeautifulSoup(r2.text, 'html.parser')

    try:
        count_doc = int(first_soup.find('span', class_='search-export__count').text.split(': ')[1])
        print('1111111')

    except:
        count_doc = 0

    if count_doc > 0:
        count_doc = count_doc // 15 + 1
        # print(count_doc)

        # with open("sogl.html", "w") as file:
        #     file.write(r2.text)

        i = 1
        k = 0
        queue = Queue()
        processes = []
        df_list = []
        df_final = pd.DataFrame()

        for i in range(1, count_doc + 1):
            p = Process(target=sogly, args=(s, DNSID, i, queue))
            p.start()
            processes.append(p)

        for i in range(1, count_doc + 1):
            df = queue.get()
            df_list.append(df)

        for p in processes:
            p.join()

        df_final = pd.concat(df_list)
        df_final.to_excel('test_report_sogl.xlsx')
        # print(df_final)
        documents = df_final['doc_id'].to_list()
        queue = Queue()
        processes = []
        df_list = []
        # print(documents)
        df_status = pd.DataFrame()
        if FIO == 'Биктимиров Р.Г.':
            for i in range(len(documents)):
                p = Process(target=sogl_response_rg, args=(s, documents[i], DNSID, queue))
                p.start()
                processes.append(p)

            for i in range(len(documents)):
                df = queue.get()
                df_list.append(df)

            for p in processes:
                p.join()

            df_status = pd.concat(df_list)
            print(df_status)
            df_final = pd.merge(df_final, df_status, on='doc_id', how='left')
            df_final.drop(['Дата согла', 'Адресат', 'doc_id', 'link_id'], axis=1, inplace=True)

        if FIO == 'Мусиенко О.А.':
            for i in range(len(documents)):
                p = Process(target=sogl_response_oa, args=(s, documents[i], DNSID, queue))
                p.start()
                processes.append(p)

            for i in range(len(documents)):
                df = queue.get()
                df_list.append(df)

            for p in processes:
                p.join()

            df_status = pd.concat(df_list)
            print(df_status)
            df_final = pd.merge(df_final, df_status, on='doc_id', how='left')
            df_final.drop(['Дата согла', 'Адресат', 'doc_id', 'link_id'], axis=1, inplace=True)

        # df_status = pd.concat(df_list)
        # print(df_status)
        # df_final = pd.merge(df_final, df_status, on='doc_id', how='left')
        # df_final.drop(['Дата согла', 'Адресат', 'doc_id', 'link_id'], axis=1, inplace=True)
        df_final.to_excel(os.getcwd()+f'\\sogl_report\\{FIO}_sogl_report.xlsx')
    else:
        print('DRUGOE')
        df_final = pd.DataFrame(columns=['Номер согла','Краткое содержание','na nomer','Срок МФ/Срок РГ','Срок РГ/Срок ОА','Срок исполнителя'])
        df_final.to_excel(os.getcwd() + f'\\sogl_report\\{FIO}_sogl_report.xlsx')
    data_module.set_dnsid(DNSID)
    return os.getcwd() + f'\\sogl_report\\{FIO}_sogl_report.xlsx'


def sogly(s, DNSID, page, queue):
    url = f'https://mosedo.mos.ru/document.php?perform_search=1&DNSID={DNSID}&page={page}'
    r1 = s.get(url)
    # with open("sogl1.html", "w") as file:
    #     file.write(r1.text)
    #print(r1.text)
    soup = BeautifulSoup(r1.text, "html.parser")
    allNews = soup.find('table', class_='document-list')
#    print(allNews)
    allNews = allNews.find('tbody')
    allNews1 = BeautifulSoup(str(allNews), "html.parser")
    doc_number = [element.text for element in allNews1.find_all(class_="main_doc_table-doc-number")]
    doc_recipient = [element.text.replace('Кому:','') for element in allNews1.find_all('span', class_="s-doc__recipient")]
    short_data = [element.text for element in allNews1.find_all('div', class_="s-table__shortcontent")]
    doc_id = [element['href'] for element in allNews1.find_all('a', class_='document-list__registration-date')]
    doc_date = []

    for i in range(len(doc_number)):
        doc_number[i] = doc_number[i].replace('\n','')
        doc_number[i] = ' '.join(doc_number[i].split())
        doc_number[i] = doc_number[i].lstrip()
        doc_number[i] = doc_number[i].rstrip()
        try:
            doc_date.append(datetime.strptime(doc_number[i].split()[1], '%d.%m.%Y'))
        except:
            doc_date.append('')
        doc_number[i] = doc_number[i].split()[0]
    
    for i in range(len(doc_recipient)):
        doc_recipient[i] = doc_recipient[i].replace('\n','')
        doc_recipient[i] = ' '.join(doc_recipient[i].split())
        doc_recipient[i] = doc_recipient[i].lstrip()
        doc_recipient[i] = doc_recipient[i].rstrip()

    for i in range(len(short_data)):
        short_data[i] = short_data[i].replace('\n','')
        short_data[i] = ' '.join(short_data[i].split())
        short_data[i] = short_data[i].lstrip()
        short_data[i] = short_data[i].rstrip()
    
    for i in range(len(doc_id)):
        doc_id[i] = doc_id[i].replace('\n','')
        doc_id[i] = ' '.join(doc_id[i].split())
        doc_id[i] = doc_id[i].lstrip()
        doc_id[i] = doc_id[i].rstrip()   
        doc_id[i] = doc_id[i].split('=')[1]
        doc_id[i] = doc_id[i].split('&')[0]
    
    data = []

    for a, b, c, d, e, in zip(doc_number, doc_date, doc_recipient, short_data, doc_id):
        data.append([a, b, c, d, e, ])

    df1 = pd.DataFrame(data, columns=['Номер согла', 'Дата согла', 'Адресат', 'Краткое содержание', 'doc_id'])
    #print(df1)
    queue.put(df1)


def sogl_status(s, doc_number, DNSID, queue):
    url = f'https://mosedo.mos.ru/document.card.php?id={doc_number}&DNSID={DNSID}'
    r1 = s.get(url)
    soup = BeautifulSoup(r1.text, "html.parser")
    sogl = soup.findAll('table', class_='agreetable')
    doc_card = soup.find('table', class_='scrollable-section')
    doc_card_soup = BeautifulSoup(str(doc_card), "html.parser")
    doc_card = doc_card_soup.find('div', id='inNumberListContainer')
    #print(doc_card)
    doc_card_soup = BeautifulSoup(str(doc_card), "html.parser")
    registration = soup.find('a', class_='s-agree-subcomment__link')
    if registration:
        try:
            registration_status = registration.text
            registration_status = registration_status.replace('\n','')
            registration_status = ' '.join(registration_status.split())
            registration_status = registration_status.lstrip()
            registration_status = registration_status.rstrip()
        except: registration_status = '-'
    else: registration_status = '-'

    try:
        resp_doc = [doc_card_soup.find('a', class_="document-badge").text]
        on_number_link = doc_card_soup.find('a', class_="document-badge")['href']
    except:
        resp_doc = ['-']
        on_number_link = ''
    
    for i in range(len(resp_doc)):
        if resp_doc[i]=='':
            resp_doc[i] = '-'
        resp_doc[i] = resp_doc[i].replace('\n','')
        resp_doc[i] = ' '.join(resp_doc[i].split())
        resp_doc[i] = resp_doc[i].lstrip()
        resp_doc[i] = resp_doc[i].rstrip()   
        
    if len(resp_doc) < 1:
        resp_doc.append('-')

    sogl_soup = BeautifulSoup(str(sogl), "html.parser")
    sogl_user = [element.text for element in sogl_soup.find_all('b', class_="agreetable__user-name")]
    sogl_status = [element.text for element in sogl_soup.find_all('span', class_="csdr-status")]
    sogl_date = []

    for i in range(len(sogl_user)):
        if sogl_user[i]=='':
            sogl_user[i] = '-'
        sogl_user[i] = sogl_user[i].replace('\n','')
        sogl_user[i] = ' '.join(sogl_user[i].split())
        sogl_user[i] = sogl_user[i].lstrip()
        sogl_user[i] = sogl_user[i].rstrip()
        
    for i in range(len(sogl_status)):
        if sogl_status[i]=='':
            sogl_status[i] = '-'
        sogl_status[i] = sogl_status[i].replace('\n','')
        sogl_status[i] = ' '.join(sogl_status[i].split())
        sogl_status[i] = sogl_status[i].lstrip()
        sogl_status[i] = sogl_status[i].rstrip()
        try:
            sogl_date.append(datetime.strptime(sogl_status[i].split()[1] + ' ' + sogl_status[i].split()[2], '%d.%m.%Y %H:%M'))
        except:
            sogl_date.append('')
        
        if r'Подписан' in sogl_status[i]:
            sogl_status[i] = sogl_status[i].split()[0]
            
        if r'Не согласов' in sogl_status[i]:
            sogl_status[i] = sogl_status[i].split()[0] + ' ' + sogl_status[i].split()[1]

#    print(sogl_status)
    datata = []
    for a, b, c, in zip(sogl_user, sogl_status, sogl_date):
        datata.append([a, b, c, ])
    #print(datata)
    df = pd.DataFrame(datata, columns=['Пользователь','Статус', 'Время статуса'])
    df.insert(2, 'На №', resp_doc[0])
    statuslist = df['Время статуса'].to_list()
    resp_list = df['На №'].to_list()
    statuslist = [item for item in statuslist if pd.isnull(item) == False]
    resp_list = [item for item in resp_list if pd.isnull(item) == False]
    #print(df['Статус'])
#    a=input()
    df_new = df.loc[df['Статус'] == r'На согласовании/подписании']
    if df_new.empty == False:
        df_new['Время статуса'] = statuslist[-1]
        df_new['На №'] = resp_list[-1]
    if df_new.empty:
        #print(df)
        df_new = df.loc[df['Статус'].str.contains(r'Подписан')]
        df_new['Время статуса'] = statuslist[-1]
        df_new['На №'] = resp_list[-1]
    if df_new.empty:
        df_new = df.loc[df['Статус'].str.contains(r'Не согласов')]
        df_new['Время статуса'] = statuslist[-1]
        df_new['На №'] = resp_list[-1]
    if df_new.empty:
        df_new = df.loc[df['Статус'].str.contains(r'На подписа')]
        df_new['Время статуса'] = statuslist[-1]
        df_new['На №'] = resp_list[-1]
    if df_new.empty:
        df_new = pd.DataFrame({'Пользователь':['-'],'Статус':['-'], 'На №':[resp_list[-1]]})
    del df
    df_new.insert(0, 'doc_id', doc_number)
    df_new.insert(4, 'regisrtation', registration_status)
    queue.put(df_new)


def sogl_response_rg(s, doc_number, DNSID, queue):
    url = f'https://mosedo.mos.ru/document.card.php?id={doc_number}&DNSID={DNSID}'
    r1 = s.get(url)
    soup = BeautifulSoup(r1.text, "html.parser")
    doc_card = soup.find('table', class_='scrollable-section')
    doc_card_soup = BeautifulSoup(str(doc_card), "html.parser")
    doc_card = doc_card_soup.find('div', id='inNumberListContainer')

    doc_card_soup = BeautifulSoup(str(doc_card), "html.parser")

    try:
        resp_doc = [doc_card_soup.find('a', class_="document-badge").text]
        on_number_link = [doc_card_soup.find('a', class_="document-badge")['href']]
    except:
        resp_doc = ['-']
        on_number_link = ['-']

    for i in range(len(resp_doc)):
        if resp_doc[i] == '':
            resp_doc[i] = '-'
        resp_doc[i] = resp_doc[i].replace('\n', '')
        resp_doc[i] = ' '.join(resp_doc[i].split())
        resp_doc[i] = resp_doc[i].lstrip()
        resp_doc[i] = resp_doc[i].rstrip()
        resp_doc[i] = resp_doc[i].split(' от')[0]

    if len(resp_doc) < 1:
        resp_doc.append('-')
    doc_number_list = [doc_number]
    for i in range(len(on_number_link)):
        if on_number_link[i] != '-':
            on_number_link[i] = on_number_link[i].replace('\n','')
            on_number_link[i] = ' '.join(on_number_link[i].split())
            on_number_link[i] = on_number_link[i].lstrip()
            on_number_link[i] = on_number_link[i].rstrip()
            on_number_link[i] = on_number_link[i].split('=')[1]
            on_number_link[i] = on_number_link[i].split('&')[0]
    data_docs = deadline_check_rg(s, DNSID, on_number_link[0])
    datata = []
    for a, b, c, in zip(resp_doc, on_number_link, doc_number_list):
        datata.append([a, b, c, data_docs[0], data_docs[1], data_docs[2]])
    df = pd.DataFrame(datata, columns=['na nomer', 'link_id', 'doc_id', 'срок МФ', 'срок РГ', 'Исполнитель'])
    queue.put(df)

def sogl_response_oa(s, doc_number, DNSID, queue):
    url = f'https://mosedo.mos.ru/document.card.php?id={doc_number}&DNSID={DNSID}'
    r1 = s.get(url)
    soup = BeautifulSoup(r1.text, "html.parser")
    doc_card = soup.find('table', class_='scrollable-section')
    doc_card_soup = BeautifulSoup(str(doc_card), "html.parser")
    doc_card = doc_card_soup.find('div', id='inNumberListContainer')

    doc_card_soup = BeautifulSoup(str(doc_card), "html.parser")

    try:
        resp_doc = [doc_card_soup.find('a', class_="document-badge").text]
        on_number_link = [doc_card_soup.find('a', class_="document-badge")['href']]
    except:
        resp_doc = ['-']
        on_number_link = ['-']

    for i in range(len(resp_doc)):
        if resp_doc[i] == '':
            resp_doc[i] = '-'
        resp_doc[i] = resp_doc[i].replace('\n', '')
        resp_doc[i] = ' '.join(resp_doc[i].split())
        resp_doc[i] = resp_doc[i].lstrip()
        resp_doc[i] = resp_doc[i].rstrip()
        resp_doc[i] = resp_doc[i].split(' от')[0]

    if len(resp_doc) < 1:
        resp_doc.append('-')
    doc_number_list = [doc_number]
    for i in range(len(on_number_link)):
        if on_number_link[i] != '-':
            on_number_link[i] = on_number_link[i].replace('\n', '')
            on_number_link[i] = ' '.join(on_number_link[i].split())
            on_number_link[i] = on_number_link[i].lstrip()
            on_number_link[i] = on_number_link[i].rstrip()
            on_number_link[i] = on_number_link[i].split('=')[1]
            on_number_link[i] = on_number_link[i].split('&')[0]
    data_docs = deadline_check_oa(s, DNSID, on_number_link[0])
    datata = []
    for a, b, c, in zip(resp_doc, on_number_link, doc_number_list):
        datata.append([a, b, c, data_docs[0], data_docs[1], data_docs[2]])
    df = pd.DataFrame(datata, columns=['na nomer', 'link_id', 'doc_id', 'срок РГ', 'срок ОА', 'Исполнитель'])
    queue.put(df)


def deadline_check_rg(s, DNSID, doc_id):
    warnings.filterwarnings('ignore')
    url = f'https://mosedo.mos.ru/document.card.php?id={doc_id}&DNSID={DNSID}'
    r2 = s.get(url)
    # print (r2.text)
    doc_soup = BeautifulSoup(r2.text, 'html.parser').find('table', id='rez-list')
    print(doc_id)

    try:
        list_DS = doc_soup.findAll('span', class_='resolution-executor-history')
    except:
        list_DS = ['DSP']
    executor = []

    try:
        author_DS = doc_soup.findAll('div', class_='resolution-item__header')

        for item in author_DS:
            if not item.parent.find('div', class_='resolution-item__vzamen'):

                if item.find('span'):
                    if item.find('span').find('span'):
                        if 'Биктимиров Р.Г.' in item.find('span').find('span').text:
                            if item.parent.find('span', class_='resolution-executor-history'):
                                in_res = item.parent.findAll('span', class_='resolution-executor-history')
                                for res in in_res:
                                    try:
                                        executor.append(res.text.replace('\n', ' '))
                                    except:
                                        executor.append('-')
                            #                        executor.append(item.parent.find('span', class_='resolution-executor-history').text.replace('\n',' '))
                            else:
                                executor.append('-')
                        else:
                            executor.append('-')
                    else:
                        executor.append('-')
                else:
                    executor.append('-')
            else:
                if 'Резолюция отменена' not in item.parent.find('div', class_='resolution-item__vzamen').get_text():
                    if item.find('span'):
                        if item.find('span').find('span'):
                            if 'Биктимиров Р.Г.' in item.find('span').find('span').text:
                                if item.parent.find('span', class_='resolution-executor-history'):
                                    in_res = item.parent.findAll('span', class_='resolution-executor-history')
                                    for res in in_res:
                                        try:
                                            executor.append(res.text.replace('\n', ' '))
                                        except:
                                            executor.append('-')
                                #                        executor.append(item.parent.find('span', class_='resolution-executor-history').text.replace('\n',' '))
                                else:
                                    executor.append('-')
                            else:
                                executor.append('-')
                        else:
                            executor.append('-')
                    else:
                        executor.append('-')
                else:
                    executor.append('-')
                    print(item.parent.find('div', class_='resolution-item__vzamen').get_text())
    except:
        executor.append('Документ ДСП')
    print(executor)
    df = pd.DataFrame(columns=['A', 'B', 'C'])
    if 'DSP' not in list_DS:
        for item in list_DS:
            data = []
            gr = item.text
            gr = gr.replace('\n', ' ')
            gr = ' '.join(gr.split())
            gr = gr.lstrip()
            gr = gr.rstrip()
            gr = gr.split(' - ')
            if 'змене' in gr[2]:
                data.append(gr[0])
                data.append(datetime.strptime(gr[2].split(': ')[1], '%d.%m.%Y'))
                data.append(gr[3])
            else:
                data.append(gr[0])
                data.append(datetime.strptime(gr[1].split(': ')[1], '%d.%m.%Y'))
                data.append(gr[2])
            df.loc[len(df.index)] = data
    else:
        df.loc[len(df.index)] = ['Документ ДСП', 'Документ ДСП', 'Документ ДСП']
    df = df[df['C'].str.contains('снят с контроля') == False]
    df = df.drop_duplicates(keep='first')
    print(df)
    df_RG = df[df['A'].str.contains('Биктимиров')]
    sroki_RG = df_RG['B'].to_list()

    if df_RG.empty == False:
        df_RG.sort_values(by='B', inplace=True)
        sroki_RG = df_RG['B'].to_list()
        for i in range(len(sroki_RG)):
            if not isinstance(sroki_RG[i], datetime):
                pass
            else:
                sroki_RG[i] = datetime.strftime(sroki_RG[i], '%d.%m.%Y')
        srok_rg = '\n'.join(sroki_RG)
    else:
        srok_rg = '-'

    df_RG = df[df['A'].str.contains('Гаман')]

    if df_RG.empty == False:
        df_RG.sort_values(by='B', inplace=True)
        sroki_RG = df_RG['B'].to_list()
        for i in range(len(sroki_RG)):
            if not isinstance(sroki_RG[i], datetime):
                pass
            else:
                sroki_RG[i] = datetime.strftime(sroki_RG[i], '%d.%m.%Y')
        srok_mf = '\n'.join(sroki_RG)
    else:
        srok_mf = '-'


    if 'Документ ДСП' not in executor:
        i = len(executor) - 1
        i = len(executor) - 1
        while i >= 0:
            try:
                executor.remove('-')
            except:
                pass
            i = i - 1
        i = len(executor) - 1
        df_exec_list = []
        if len(executor) == 0:
            executor.append('-')
            df_exec = pd.DataFrame({'A': ['-'], 'B': ['-'], 'C': ['-']})
            df_exec_list.append(df_exec)

        else:
            for j in range(len(executor)):
                df_exec1 = pd.DataFrame(columns=['A', 'B', 'C'])
                #            print(executor[i])

                executor_one = executor[j].replace('\n', ' ')
                executor_one = ' '.join(executor_one.split())
                executor_one = executor_one.lstrip()
                executor_one = executor_one.rstrip()
                executor_one = executor_one.split(' - ')
                # if executor_one == 'Габитов Д.Ш.':
                #     executor_one = '-'
                executor1 = []
                if executor_one != '-':
                    #                if len(executor_one) < 3:
                    #                    print('!!!!!!!!!!!!!!!!    ',executor_one)


                    if 'змене' in executor_one[2]:
                        executor1.append(executor_one[0])
                        executor1.append(datetime.strptime(executor_one[2].split(': ')[1], '%d.%m.%Y'))
                        executor1.append(executor_one[3])
                    else:
                        executor1.append(executor_one[0])
                        executor1.append(datetime.strptime(executor_one[1].split(': ')[1], '%d.%m.%Y'))
                        executor1.append(executor_one[2])
                else:
                    executor1.append('-')
                    executor1.append('-')
                    executor1.append('-')

                df_exec1 = pd.DataFrame([executor1], columns=['A', 'B', 'C'])
                df_exec_list.append(df_exec1)
        print('----------------', len(df_exec_list), '-------------')
        if len(df_exec_list) > 1:
            df_executor = pd.concat(df_exec_list)
        else:
            df_executor = df_exec_list[0]
        #    else:
        #        df_executor = pd.DataFrame({'A':['-'],'B':['-'],'C':['-']})

        if len(df_executor) > 1:
            df_executor = df_executor.sort_values(by='B')
        df_executor = df_executor.loc[df_executor['C'].str.contains('снят с контроля') == False]
        executor_date = df_executor['B'].to_list()
        executor_name = df_executor['A'].to_list()
        executor = []
        for i in range(len(executor_date)):
            if executor_date[i] == '-':
                executor.append('-')
            else:
                executor.append(datetime.strftime(executor_date[i], '%d.%m.%Y') + ' (' + executor_name[i] + ')')
        executor_str = '\n'.join(executor)
        # df_executor.to_excel(f'{doc_id}.xlsx')
        # df_executor = df_executor.iloc[0]
        # print(df_executor.head())
        # executor = df_executor.to_list()

        ###################################################################################################################################################
        data = [srok_mf, srok_rg, executor_str]
    else:
        data = [srok_mf, srok_rg, 'Документ ДСП']

    if doc_id == '-':
        data = ['-', '-', '-']
    #df2 = pd.DataFrame([data], columns=['link', 'mf', 'rg', 'executor'])

    return data


def deadline_check_oa(s, DNSID, doc_id):
    warnings.filterwarnings('ignore')
    url = f'https://mosedo.mos.ru/document.card.php?id={doc_id}&DNSID={DNSID}'
    r2 = s.get(url)
    # print (r2.text)
    doc_soup = BeautifulSoup(r2.text, 'html.parser').find('table', id='rez-list')
    print(doc_id)

    try:
        list_DS = doc_soup.findAll('span', class_='resolution-executor-history')
    except:
        list_DS = ['DSP']
    executor = []

    try:
        author_DS = doc_soup.findAll('div', class_='resolution-item__header')

        for item in author_DS:
            if not item.parent.find('div', class_='resolution-item__vzamen'):

                if item.find('span'):
                    if item.find('span').find('span'):
                        if 'Мусиенко О.А.' in item.find('span').find('span').text:
                            if item.parent.find('span', class_='resolution-executor-history'):
                                in_res = item.parent.findAll('span', class_='resolution-executor-history')
                                for res in in_res:
                                    try:
                                        executor.append(res.text.replace('\n', ' '))
                                    except:
                                        executor.append('-')
                            #                        executor.append(item.parent.find('span', class_='resolution-executor-history').text.replace('\n',' '))
                            else:
                                executor.append('-')
                        else:
                            executor.append('-')
                    else:
                        executor.append('-')
                else:
                    executor.append('-')
            else:
                if 'Резолюция отменена' not in item.parent.find('div', class_='resolution-item__vzamen').get_text():
                    if item.find('span'):
                        if item.find('span').find('span'):
                            if 'Мусиенко О.А.' in item.find('span').find('span').text:
                                if item.parent.find('span', class_='resolution-executor-history'):
                                    in_res = item.parent.findAll('span', class_='resolution-executor-history')
                                    for res in in_res:
                                        try:
                                            executor.append(res.text.replace('\n', ' '))
                                        except:
                                            executor.append('-')
                                #                        executor.append(item.parent.find('span', class_='resolution-executor-history').text.replace('\n',' '))
                                else:
                                    executor.append('-')
                            else:
                                executor.append('-')
                        else:
                            executor.append('-')
                    else:
                        executor.append('-')
                else:
                    executor.append('-')
                    print(item.parent.find('div', class_='resolution-item__vzamen').get_text())
    except:
        executor.append('Документ ДСП')
    print(executor)
    df = pd.DataFrame(columns=['A', 'B', 'C'])
    if 'DSP' not in list_DS:
        for item in list_DS:
            data = []
            gr = item.text
            gr = gr.replace('\n', ' ')
            gr = ' '.join(gr.split())
            gr = gr.lstrip()
            gr = gr.rstrip()
            gr = gr.split(' - ')
            if 'змене' in gr[2]:
                data.append(gr[0])
                data.append(datetime.strptime(gr[2].split(': ')[1], '%d.%m.%Y'))
                data.append(gr[3])
            else:
                data.append(gr[0])
                data.append(datetime.strptime(gr[1].split(': ')[1], '%d.%m.%Y'))
                data.append(gr[2])
            df.loc[len(df.index)] = data
    else:
        df.loc[len(df.index)] = ['Документ ДСП', 'Документ ДСП', 'Документ ДСП']
    df = df[df['C'].str.contains('снят с контроля') == False]
    df = df.drop_duplicates(keep='first')
    print(df)
    df_RG = df[df['A'].str.contains('Мусиенко')]
    sroki_RG = df_RG['B'].to_list()

    if df_RG.empty == False:
        df_RG.sort_values(by='B', inplace=True)
        sroki_RG = df_RG['B'].to_list()
        for i in range(len(sroki_RG)):
            if not isinstance(sroki_RG[i], datetime):
                pass
            else:
                sroki_RG[i] = datetime.strftime(sroki_RG[i], '%d.%m.%Y')
        srok_rg = '\n'.join(sroki_RG)
    else:
        srok_rg = '-'

    df_RG = df[df['A'].str.contains('Биктимиров')]

    if df_RG.empty == False:
        df_RG.sort_values(by='B', inplace=True)
        sroki_RG = df_RG['B'].to_list()
        for i in range(len(sroki_RG)):
            if not isinstance(sroki_RG[i], datetime):
                pass
            else:
                sroki_RG[i] = datetime.strftime(sroki_RG[i], '%d.%m.%Y')
        srok_mf = '\n'.join(sroki_RG)
    else:
        srok_mf = '-'


    if 'Документ ДСП' not in executor:
        i = len(executor) - 1
        i = len(executor) - 1
        while i >= 0:
            try:
                executor.remove('-')
            except:
                pass
            i = i - 1
        i = len(executor) - 1
        df_exec_list = []
        if len(executor) == 0:
            executor.append('-')
            df_exec = pd.DataFrame({'A': ['-'], 'B': ['-'], 'C': ['-']})
            df_exec_list.append(df_exec)

        else:
            for j in range(len(executor)):
                df_exec1 = pd.DataFrame(columns=['A', 'B', 'C'])
                #            print(executor[i])

                executor_one = executor[j].replace('\n', ' ')
                executor_one = ' '.join(executor_one.split())
                executor_one = executor_one.lstrip()
                executor_one = executor_one.rstrip()
                executor_one = executor_one.split(' - ')
                # if executor_one == 'Габитов Д.Ш.':
                #     executor_one = '-'
                executor1 = []
                if executor_one != '-':
                    #                if len(executor_one) < 3:
                    #                    print('!!!!!!!!!!!!!!!!    ',executor_one)


                    if 'змене' in executor_one[2]:
                        executor1.append(executor_one[0])
                        executor1.append(datetime.strptime(executor_one[2].split(': ')[1], '%d.%m.%Y'))
                        executor1.append(executor_one[3])
                    else:
                        executor1.append(executor_one[0])
                        executor1.append(datetime.strptime(executor_one[1].split(': ')[1], '%d.%m.%Y'))
                        executor1.append(executor_one[2])
                else:
                    executor1.append('-')
                    executor1.append('-')
                    executor1.append('-')

                df_exec1 = pd.DataFrame([executor1], columns=['A', 'B', 'C'])
                df_exec_list.append(df_exec1)
        print('----------------', len(df_exec_list), '-------------')
        if len(df_exec_list) > 1:
            df_executor = pd.concat(df_exec_list)
        else:
            df_executor = df_exec_list[0]
        #    else:
        #        df_executor = pd.DataFrame({'A':['-'],'B':['-'],'C':['-']})

        if len(df_executor) > 1:
            df_executor = df_executor.sort_values(by='B')
        df_executor = df_executor.loc[df_executor['C'].str.contains('снят с контроля') == False]
        executor_date = df_executor['B'].to_list()
        executor_name = df_executor['A'].to_list()
        executor = []
        for i in range(len(executor_date)):
            if executor_date[i] == '-':
                executor.append('-')
            else:
                executor.append(datetime.strftime(executor_date[i], '%d.%m.%Y') + ' (' + executor_name[i] + ')')
        executor_str = '\n'.join(executor)
        # df_executor.to_excel(f'{doc_id}.xlsx')
        # df_executor = df_executor.iloc[0]
        # print(df_executor.head())
        # executor = df_executor.to_list()

        ###################################################################################################################################################
        data = [srok_mf, srok_rg, executor_str]
    else:
        data = [srok_mf, srok_rg, 'Документ ДСП']

    if doc_id == '-':
        data = ['-', '-', '-']
    #df2 = pd.DataFrame([data], columns=['link', 'mf', 'rg', 'executor'])

    return data


def sogl_update(FIO, EXECUTOR_ID):
    warnings.filterwarnings('ignore')
    ds = datetime.now()
    print(ds)
    d_start = '01.01.2019'
    year = datetime.now().year
    print(type(year))
    d_end = f'31.12.{year}'

    date_now = datetime.strftime(datetime.now(), '%d.%m.%Y')

    url_kontrol = f'https://mosedo.mos.ru/auth.php?uri=%2Fstat%2Fcontrol_stats.details.php%3Ffixed%3D%26delegate_id%3D%26is_letter%3D%26report_name%3Dcontrol_stats%26ctl_type%255B0%255D%3D0%26ctl_type%255B1%255D%3D1%26later_type%3D0%26due_date_from%3D{d_start}%26due_date_until%3D{d_end}%26start_rdate%3D%26end_rdate%3D%26user%255B0%255D%3D0%26inv_user%255B0%255D%3D0%26executor%3D{EXECUTOR_ID}%26inv_executor%3D0%26result%3D%25D1%25F4%25EE%25F0%25EC%25E8%25F0%25EE%25E2%25E0%25F2%25FC%2B%25EE%25F2%25F7%25E5%25F2...'
    url_auth = 'https://mosedo.mos.ru/auth.php?group_id=21'

    with open(r'C:\control_mail_2.1\settings.json') as f:
        settings = json.load(f)
        token = settings['token2']
        SEDOlog = settings['SEDOlog']
        SEDOpass = settings['SEDOpass']
        print(SEDOpass)
        PCuser = settings['PCuser']
        UserID = settings['UserID']

    s = requests.Session()

    ###########################################################################
    sogl_s_date = datetime.strftime(datetime.now() - timedelta(days=14), '%d.%m.%Y')
    sogl_end_date = datetime.strftime(datetime.now(), '%d.%m.%Y')

    DNSID = data_module.get_dnsid() #data_module.get_dnsid()  ##wMsWJe-80daXYVWU4d8u_FA  ##w3YG8nxy3qvMCbxDc5lUM5Q
    # DNSID = 'wjxPHErZC0ulvM6xPEtG6Zg'

    data = {"DNSID": DNSID,
            "group_id": "21",
            "login": SEDOlog,  # %C0%F0%F1%E5%ED%FC%E5%E2+%C2.%C4.
            "user_id": "80742170",  ##80742170 Арсеньев ##78264321 Габитов
            "password": SEDOpass,
            "token": "",
            "x": "1"}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Connection': 'keep-alive', }

    data_DS = {
        'check_all_projects': 'on',
        'project_type_1': '1',
        'project_type_3': '1',
        'project_type_13': '1',
        'project_type_4': '1',
        'project_type_5': '1',
        'has_period': '1',
        'year_from': '2009',
        'year_to': f'{str(year)}',
        'order_by': 'default',
        'required_text': '',
        'num': '',
        'rdate_f': '',
        'org_name': '%C4%C3%C8%E3%CC',
        'org': '21',
        'rdate_t': '',
        'reg_user': '',
        'reg_user_id': '',
        'recipient': '',
        'recipient_id': '',
        'recipient_group': '',
        'recipient_group_id': '',
        'in_number': '',
        'bound_number': '',
        'contract_bound_number': '',
        'recipient_org_id': '',
        'cl_out_num': '',
        'cl_out_date_f': '',
        'cl_out_date_t': '',
        'cl_sign': '',
        'cl_sign_id': '',
        'cl_sign_group': '',
        'cl_sign_group_id': '',
        'cl_executor': '',
        'cl_executor_id': '',
        'cl_executor_group': '',
        'cl_executor_group_id': '',
        'cl_text': '',
        'out_number': '',
        'out_date_f': '',
        'out_reg_user': '',
        'out_reg_user_id': '',
        'out_date_t': '',
        'author': '',
        'author_id': '',
        'author_group': '',
        'author_group_id': '',
        'prepared_by': '',
        'prepared_by_id': '',
        'prepared_by_org_id': '',
        'curator': '',
        'curator_id': '',
        'short_content': '',
        'document_kind': '0',
        'delivery_type': '',
        'document_special_kind': '0',
        'external_id': '',
        'has_manual_sign': '0',
        'is_hand_shipping': '0',
        'sign_type': '0',
        'is_dsp': '0',
        'is_control': '0',
        'is_urgent': '0',
        'creator': '',
        'creator_id': '',
        'memo': '',
        'send_date_f': '',
        'send_date_t': '',
        'info': '',
        'info_author': '',
        'info_author_id': '',
        'info_date_f': '',
        'info_date_t': '',
        'og_file_number': '0',
        'rec_vdelo': '0',
        'vdelo_date_f': '',
        'vdelo_date_t': '',
        'vdelo_prepared': '',
        'vdelo_prepared_id': '',
        'vdelo_signed': '',
        'vdelo_signed_id': '',
        'vdelo_text': '',
        'res_type': '0',
        'res_urgency': '0',
        'resolution_num': '',
        'r_rdate_f': '',
        'resolution_creator': '',
        'resolution_creator_id': '',
        'r_rdate_t': '',
        'resolution_author': '',
        'resolution_author_id': '',
        'resolution_author_group': '',
        'resolution_author_group_id': '',
        'resolution_author_org_id': '',
        'r_special_control': '0',
        'resolution_behalf': '',
        'resolution_behalf_id': '',
        'resolution_acting_author': '',
        'resolution_acting_author_id': '',
        'resolution_to': '',
        'resolution_to_id': '',
        'resolution_to_group': '',
        'resolution_to_group_id': '',
        'resolution_to_org_id': '',
        'res_project_letter': '0',
        'res_curator': '',
        'res_curator_id': '',
        'r_control': '0',
        'r_control_f': '',
        'r_control_t': '',
        'r_otv': '0',
        'r_dback': '0',
        'resolution_text': '',
        'r_ef_reason_category_id': '0',
        'r_ef_reason_id': '0',
        'r_is_signed': '0',
        'r_plus': '0',
        'r_another_control': '0',
        'r_oncontrol': '0',
        'r_oncontrol_f': '',
        'r_oncontrol_t': '',
        'unset_control': '0',
        'unset_control_f': '',
        'unset_control_t': '',
        're_date_f': '',
        're_date_t': '',
        're_author': '',
        're_author_id': '',
        're_author_group': '',
        're_author_group_id': '',
        're_acting_author': '',
        're_acting_author_id': '',
        're_is_interim': '-1',
        're_text': '',
        'docs_in_execution': '0',
        're_doc_org_id': '',
        'csdr_initiator': '',
        'csdr_initiator_id': '',
        'csdr_initiator_group': '',
        'csdr_initiator_group_id': '',
        'csdr_start': '0',
        'csdr_start_date_f': '',
        'csdr_start_date_t': '',
        'csdr_stop': '2',
        'csdr_current_version_only': '1',
        'and[csdr][0]': '0',
        'participant_name_0': FIO,
        'participant_name_0_id': EXECUTOR_ID,
        'participant_group_0': '%C4%E5%EF%E0%F0%F2%E0%EC%E5%ED%F2+%E3%EE%F0%EE%E4%F1%EA%EE%E3%EE+%E8%EC%F3%F9%E5%F1%F2%E2%E0+%E3%EE%F0%EE%E4%E0+%CC%EE%F1%EA%E2%FB',
        'participant_group_0_id': '21',
        'csdr_has_deadline_0': '0',
        'csdr_status_0': '2',
        'csdr_init_date_0_f': '',
        'csdr_init_date_0_t': ''
    }



    r = s.post(url_auth, data=data, headers=headers, allow_redirects=False)
    data_module.set_dnsid(DNSID)
    DNSID = r.headers['location'].split('DNSID=')[1]
    # auth_token = s.cookies.get_dict()['auth_token']
    #s.cookies
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Connection': 'keep-alive',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
    }
    url_sogl = f'https://mosedo.mos.ru/document_search.php?new=0&DNSID={DNSID}'
    r2 = s.post(url_sogl, data=data_DS, headers=headers2)
    with open("sogl1.html", "w") as file:
        file.write(r2.text)
    first_soup = BeautifulSoup(r2.text, 'html.parser')
    try:
        count_doc = int(first_soup.find('span', class_='search-export__count').text.split(': ')[1])
        print('1111111')
    except:
        count_doc = 0
    if count_doc > 0:
        count_doc = count_doc // 15 + 1
        # print(count_doc)

        # with open("sogl.html", "w") as file:
        #     file.write(r2.text)

        i = 1
        k = 0
        queue = Queue()
        processes = []
        df_list = []
        df_final = pd.DataFrame()

        for i in range(1, count_doc + 1):
            p = Process(target=sogly, args=(s, DNSID, i, queue))
            p.start()
            processes.append(p)

        for i in range(1, count_doc + 1):
            df = queue.get()
            df_list.append(df)

        for p in processes:
            p.join()

        df_final = pd.concat(df_list)
        # print(df_final)
        documents = df_final['doc_id'].to_list()
        queue = Queue()
        processes = []
        df_list = []
        # print(documents)
        df_status = pd.DataFrame()

        for i in range(len(documents)):
            p = Process(target=sogl_status, args=(s, documents[i], DNSID, queue))
            p.start()
            processes.append(p)

        for i in range(len(documents)):
            df = queue.get()
            df_list.append(df)

        for p in processes:
            p.join()

        df_status = pd.concat(df_list)
        df_final = pd.merge(df_final, df_status, on='doc_id', how='left')
        df_final = df_final.loc[pd.isna(df_final['Статус']) == False]
        df_final = df_final.loc[df_final['Пользователь'] == FIO]
        statuses = ['На согласовании/подписании', 'На подписании']
        df_final = df_final.loc[df_final['Статус'].isin(statuses)]
        # df_final.to_excel(r'C:\control_mail_2.1\sogl_ds.xlsx', index=False)
        s.close()
    else:
        df_final = pd.DataFrame()
    de = datetime.now()
    print(de)
    # print('\n')
    print(de - ds)
    #print(df_final.info)
    data_module.set_dnsid(DNSID)
    if not df_final.empty:
        df_final.sort_values(by=['Дата согла'], ascending=False, inplace=True)
        df_final_today = df_final.loc[df_final['Дата согла'] == datetime.strftime(datetime.now(), '%d.%m.%Y')]
        df_final_older = df_final.loc[df_final['Дата согла'] != datetime.strftime(datetime.now(), '%d.%m.%Y')]
        print(df_final_older.info)
        line = 'Соглы, требующие Вашего внимания, от новых к старым:'
        rez_today = '\n'
        rez_older = '\n'

        if not df_final_today.empty:
            lst_line_today = df_final_today['Номер согла'].to_list()
            text_today = df_final_today['Краткое содержание'].to_list()

            for i in range(len(lst_line_today)):
                lst_line_today[i] = str(i+1) + ') ' + lst_line_today[i]

            lst_line_today.insert(0, '\n---------------------\nСоглы, запущенные сегодня:')
            rez_today = '\n'.join(lst_line_today)

        if not df_final_older.empty:
            lst_line_older = df_final_older['Номер согла'].to_list()
            text_older = df_final_older['Краткое содержание'].to_list()

            for i in range(len(lst_line_older)):
                lst_line_older[i] = str(i+1) + ') ' + lst_line_older[i]

            lst_line_older.insert(0, '\n---------------------\nСоглы, запущенные вчера и ранее:')
            rez_older = '\n'.join(lst_line_older)
        rez = line+rez_today+rez_older
        del line

        if len(rez) > 1023:
            sogl_number = df_final['Номер согла'].to_list()
            sogl_date = df_final['Дата согла'].to_list()
            for i in range(len(sogl_date)):
                sogl_date[i] = datetime.strftime(sogl_date[i], '%d.%m.%Y')
            sogl_text = df_final['Краткое содержание'].to_list()
            number = 1
            html = ''

            for i in range(len(sogl_number)):
                html = html + '<tr style="height: 74px;">' \
                              f'<td class="u-table-cell">{str(number)}</td>' \
                              f'<td class="u-table-cell">{str(sogl_number[i])}</td>' \
                              f'<td class="u-table-cell">{str(sogl_date[i])}</td>' \
                              f'<td class="u-table-cell">{str(sogl_text[i])}</td>' \
                              '</tr>'
                number = number + 1
            rez = sogl_html.html1 + html + sogl_html.html2
            with open(os.getcwd() + f'/web_data/{EXECUTOR_ID}.html', 'w') as f:
                f.write(rez)
            #send_page(EXECUTOR_ID)
    else:
        rez = 'В данный момент у Вас нет соглов на рассмотрении'
    return rez


def sogl_report_send(email):
    FIO = ['Биктимиров Р.Г.', 'Мусиенко О.А.']
    EXECUTOR_ID = ['78164285', '70045']
    att_paths = []
    for i in range(len(FIO)):
        att_paths.append(sogl_report(FIO[i], EXECUTOR_ID[i]))
    print('docs done')
    print(email)
    for i in range(len(att_paths)):
        print(att_paths[i])
        file = FSInputFile(att_paths[i])
        asyncio.run(bot.send_document(email, file, caption=f'Отчет по соглам файл {str(i+1)} из {len(att_paths)}'))
        try:
            asyncio.run(bot.session.close())
        except:
            pass
    return att_paths
    # login_mail = config.EMAIL_LOG
    # password_mail = config.EMAIL_PASS
    # server = "owa.mos.ru"
    # port = 587
    # recipients = [email]
    # cc = ['ArsenevVD@mos.ru']
    #
    # mail_date = datetime.strftime(datetime.today(), '%d.%m.%Y')
    #
    # subject = 'Материалы для отчета' + mail_date
    # body = 'Материалы, сформированные автоматически'
    #
    # SMTPmail.send_email(login_mail, password_mail, server, port, recipients, cc, subject, body, att_paths)
    #
    # return 'Письмо направлено на электронную почту'


if __name__ == '__main__':
    # FIO = 'Мусиенко О.А.'
    # EXECUTOR_ID = '70045'  # 78264321 ДШ  #70045 OA #78236529 ММ #78164285 РГ #76009 Лихач
    # sogl_report(FIO, EXECUTOR_ID)
    # rez = sogl_update(FIO, EXECUTOR_ID)
    # print(rez)
    sogl_report_send(260399228)


















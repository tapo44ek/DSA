# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:01:41 2023

@author: ArsenevVD
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 08:49:07 2023

@author: ArsenevVD
"""
import selenium
from selenium import webdriver
import config
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process, Queue
import os
import time
from datetime import datetime, timedelta
import json
import pandas as pd
import requests
from base64 import b64encode
from bs4 import BeautifulSoup
import SMTPmail


def convert_to_xlsx(path_):
    with open(path_, encoding="utf8") as xml_file:
        soup = BeautifulSoup(xml_file.read(), 'html.parser')
        soup = soup.find('table')
        with open("sogl1.html", "w", encoding="utf8") as file:
            file.write(soup.text)
        columns_ = ['№', 'Источник', '№ заявки АС ГУФ', 'Время поступления', '№ заявки ДГИ', 'Дата заявки ДГИ',
                    'Дата контроля', 'Дата исполнения', 'Вид государственной услуги', 'Адрес объекта недвижимости',
                    'Заявитель', 'Исполнитель', 'Статус сбора документов', 'Округ', 'Почтовый адрес заявителя',
                    'Сведения о действующих отношениях, номер документа', 'Дата распоряжения', 'Номер распоряжения',
                    'Родительский процесс', 'Дата окончания приостановки']
        df = pd.read_html(soup.prettify())[0].iloc[4:]
        df.columns = columns_

    return df

def date_splitter(date1, date2, n):
    
    date1 = datetime.strptime(date1, '%d.%m.%Y')
    date2 = datetime.strptime(date2, '%d.%m.%Y')    
    days = date2-date1
    days = int(days.total_seconds() / 3600 / 24)
    count = days // n
    date_start_list = []
    date_end_list = [datetime.strftime(date2, '%Y-%m-%d')]
    
    for i in range(count):

        if i == 0:

            date2 = date2 - timedelta(days=n-1)
            date_start_list.append(datetime.strftime(date2, '%Y-%m-%d'))
            date2 = date2 - timedelta(days=1)
 
        if i > 0:

            date_end_list.append(datetime.strftime(date2, '%Y-%m-%d'))
            date2 = date2 - timedelta(days=n-1)
            date_start_list.append(datetime.strftime(date2, '%Y-%m-%d'))
            date2 = date2 - timedelta(days=1) 

    if days % n != 0:

        date_start_list.append(datetime.strftime(date1, '%Y-%m-%d'))
        date_end_list.append(datetime.strftime(date2, '%Y-%m-%d'))

    return date_start_list, date_end_list


def spd_stadii_sogl(user, password, AppDateFrom, AppDateTo, usluga, save_path_):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'
        }
    try:
        usluga = str(usluga)
    except:
        pass
    print('request sent ' + usluga)
    res = requests.get(f'http://{user}:{password}@webspd.mlc.gov/reports/api/Report27?AppDateFrom={AppDateFrom}&AppDateTo={AppDateTo}&AppDocsCreateDateFrom=&AppDocsCreateDateTo=&Process={usluga}&Doctype=', headers=headers)
    if res.status_code != 200:
        i = 0
        while res.status_code != 200:
            i = i + 1
            print(res.status_code, '   try number: ', i)
            time.sleep(15)
            res = requests.get(f'http://{user}:{password}@webspd.mlc.gov/reports/api/Report27?AppDateFrom={AppDateFrom}&AppDateTo={AppDateTo}&AppDocsCreateDateFrom=&AppDocsCreateDateTo=&Process={usluga}&Doctype=', headers=headers)
    print('request recieved ' + usluga)
    jsonn = json.loads(res.text)
    df = pd.DataFrame(jsonn.get('Rows'))
    df['ДатаЗаявки'] = pd.to_datetime(df['ДатаЗаявки'], format='%Y-%m-%dT%H:%M:%S')
    df['ДатаКонтроля'] = pd.to_datetime(df['ДатаКонтроля'], format='%Y-%m-%dT%H:%M:%S')
    df['ДатаОтказа'] = pd.to_datetime(df['ДатаОтказа'], format='%Y-%m-%dT%H:%M:%S')
    df['ДатаПодписи'] = pd.to_datetime(df['ДатаПодписи'], format='%Y-%m-%dT%H:%M:%S')
    df['ДатаПоследнегоСогласования'] = pd.to_datetime(df['ДатаПоследнегоСогласования'], format='%Y-%m-%dT%H:%M:%S')
    df['ДатаФормированияДокумента'] = pd.to_datetime(df['ДатаФормированияДокумента'], format='%Y-%m-%dT%H:%M:%S')


    # df[['ДатаЗаявки', 'ДатаКонтроля',
    #     'ДатаОтказа', 'ДатаПодписи',
    #     'ДатаПоследнегоСогласования',
    #     'ДатаФормированияДокумента']] = df[['ДатаЗаявки', 'ДатаКонтроля',
    #                                         'ДатаОтказа', 'ДатаПодписи',
    #                                         'ДатаПоследнегоСогласования',
    #                                         'ДатаФормированияДокумента']].apply(pd.to_datetime)
    df = df.sort_values(by='ДатаПодписи', ascending=False)
    df.to_excel(save_path_ + f'/{usluga}.xlsx', index=False)
    return df


def stadii_sogl(user, password, date_start, date_end, listuslug, headers):
    queue = Queue()
    processes = []
    df_list = []
    
    for i in range(len(listuslug)):
        
        p = Process(target=spd_stadii_sogl, args=(user, password, date_start, date_end, listuslug[i], queue, headers))
        p.start()
        processes.append(p) 
            
    for j in range(len(listuslug)):
            
        df = queue.get()
        df_list.append(df)
            
    for p in processes:
        
        p.join()
     
    try:
        merged_df = pd.concat(df_list)
    except:
        pass
    
    return merged_df
    

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def spd_ispolnenie(login_, pass_, gosusl_='0', date_start_='0', date_end_='0', compl_date_start_='0', compl_date_end_='0', spd_status_='0', save_path_='0'):
    try:
        os.remove(save_path_ + '/Applications.xls')
    except:
        pass
    gosusl_xpath_ = '//*[@id="DropDownListRegid_chzn"]/ul/li/input'
    appdate_start_xpath_ = '//*[@id="TextboxAppDate1"]'
    appdate_end_xpath_ = '//*[@id="TextboxAppDate2"]'
    compldate_start_xpath = '//*[@id="TextboxDatecomplite1"]'
    compldate_end_xpath_ = '//*[@id="TextboxDatecomplite2"]'
    status_xpath_ = '/html/body/form/div[3]/div/div[2]/div[3]/div[2]/div/div[1]/div/div/ul/li/input'


    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             "download.default_directory": save_path_,
             "directory_upgrade": True,
             "--disable-gpu": True}
    chrome_options.add_experimental_option('prefs', prefs)
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(r'http://' + login_ + ':' + pass_ + r'@webspd.mlc.gov/gosusl/gosuslweb/default.aspx')
    time.sleep(2)
    try:
        WebDriverWait(driver, 600).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content-div"]/div[1]/div[2]/a[2]'))).click()
    except:
        print("Timed out waiting for page to load")
    time.sleep(2)
    files = os.listdir(save_path_)
    files = [os.path.join(save_path_, file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    fp = max(files, key=os.path.getctime)
    while_fp = fp
    driver.find_element(By.XPATH, gosusl_xpath_).click()
    driver.find_element(By.XPATH, gosusl_xpath_).send_keys(str(gosusl_))
    time.sleep(0.5)
    driver.find_element(By.XPATH, gosusl_xpath_).send_keys(Keys.RETURN)
    time.sleep(0.2)
    if date_start_ != '0':
        driver.find_element(By.XPATH, appdate_start_xpath_).click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, appdate_start_xpath_).send_keys(date_start_)
        time.sleep(0.2)
        driver.find_element(By.XPATH, appdate_end_xpath_).click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, appdate_end_xpath_).send_keys(date_end_)
        time.sleep(0.2)
    if spd_status_ != '0':
        driver.find_element(By.XPATH, status_xpath_).click()
        driver.find_element(By.XPATH, status_xpath_).send_keys(str(spd_status_))
        time.sleep(0.5)
        driver.find_element(By.XPATH, status_xpath_).send_keys(Keys.RETURN)
        time.sleep(0.2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="LinkButton3"]').click()

    try:
        WebDriverWait(driver, 1200).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="buildings-table"]')))
    except:
        print("Timed out waiting for page to load")

    if int(driver.find_element(By.XPATH, '//*[@id="buildings-container"]/div[1]/h3/span').text) != 0:
        time.sleep(0.2)
        driver.find_element(By.XPATH, '//*[@id="content-div"]/div[1]/div/div/ul[2]/li/a').click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, '//*[@id="content-div"]/div[1]/div/div/ul[2]/li/ul/li[8]/a').click()
        while while_fp == fp:
            time.sleep(1)
            files = os.listdir(save_path_)
            files = [os.path.join(save_path_, file) for file in files]
            files = [file for file in files if os.path.isfile(file)]
            fp = max(files, key=os.path.getctime)
            time.sleep(3)
            print('YEAH')
        df_ispolnenie_ = convert_to_xlsx(save_path_ + '/Applications.xls')
        df_ispolnenie_['Время поступления'] = pd.to_datetime(df_ispolnenie_['Время поступления'],
                                                             format='%d.%m.%Y %H:%M:%S')
        df_ispolnenie_['Дата заявки ДГИ'] = pd.to_datetime(df_ispolnenie_['Дата заявки ДГИ'],
                                                             format='%d.%m.%Y')
        df_ispolnenie_['Дата контроля'] = pd.to_datetime(df_ispolnenie_['Дата контроля'],
                                                             format='%d.%m.%Y')
        df_ispolnenie_['Дата исполнения'] = pd.to_datetime(df_ispolnenie_['Дата исполнения'], format='%d.%m.%Y')

        df_ispolnenie_.to_excel(save_path_ + f'/{gosusl_}.xlsx', index=False)
        try:
            os.remove(save_path_ + '/Applications.xls')
        except:
            pass
        return df_ispolnenie_


def likhach_report(email_=''):

    with open(f'{os.getcwd()}/settings.json') as f:
        settings = json.load(f)
        user_ = settings['SPDlog']
        password_ = settings['SPDpass']
    processes = []
    att_paths = []
    #spd_ispolnenie(login_, pass_, gosusl_='0', date_start_='0', date_end_='0', compl_date_start_='0',
                  # compl_date_end_='0', spd_status_='0', save_path_='0'):
    dstart_ = datetime.strftime(datetime.now() - timedelta(days=1), '%d.%m.%Y')
    old_path_ = r'\\fsunits.mlc.gov\storez2\Управление ведения жилищного учета\3 - Отдел реализации жилищного учета\ХАЗОВ Р.Г\Отчеты\Заявки по 818 процессу в работе ' + dstart_ + '.xls'
    dstart_1_ = datetime.strftime(min(pd.read_excel(old_path_,
                                                    sheet_name='Список заявок')['Дата заявки ДГИ'].to_list()),
                                  '%d.%m.%Y')
    print(dstart_1_)
    dstart_2_ = datetime.strftime(datetime.now() - timedelta(days=30), '%d.%m.%Y')
    dend_ = datetime.strftime(datetime.now(), '%d.%m.%Y')
    print(dstart_, '\n', dstart_2_, '\n', dend_)
    # time.sleep(60)
    save_path_1_ = r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\data\likhach_report\818'
    save_path_2_ = r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\data\likhach_report\1004'
    save_path_3_ = r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\data\likhach_report\stadii_sogl'
    save_path_4_ = r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\data\likhach_report\818add'
    res_path_ = r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\data\likhach_report\result'
    print(1)
    p = Process(target=spd_stadii_sogl, args=(user_, password_, dstart_1_, dend_, '818', save_path_3_))
    p.start()
    processes.append(p)
    time.sleep(1)
    print(2)

    p = Process(target=spd_stadii_sogl, args=(user_, password_, dstart_2_, dend_, '1004', save_path_3_))
    p.start()
    processes.append(p)
    time.sleep(1)
    print(3)

    p = Process(target=spd_ispolnenie, args=(user_, password_, '818', dstart_, dend_, '0', '0', '0', save_path_1_))
    p.start()
    processes.append(p)
    time.sleep(1)

    # p = Process(target=spd_ispolnenie, args=(user_, password_, '818', dstart_1_, dend_, '0', '0', '0', save_path_4_))
    # p.start()
    # processes.append(p)

    p = Process(target=spd_ispolnenie, args=(user_, password_, '1004', '0', '0', '0', '0', 'Не выполнена', save_path_2_))
    p.start()
    processes.append(p)
    time.sleep(3)

    for p in processes:
        p.join()

    df818 = pd.read_excel(save_path_1_ + r'\818.xlsx')
    df818.info()

    df818.drop(['№ заявки АС ГУФ', 'Дата исполнения', 'Адрес объекта недвижимости', 'Исполнитель',
                'Статус сбора документов', 'Округ'], axis=1, inplace=True)

    df818.insert(4, '№ заявки ДГИ.1', df818['№ заявки ДГИ'].apply(lambda x: x.split('-(')[0]))
    df818.insert(11, 'План', '')
    df818.insert(12, 'Исполнитель', '')
    df818old = pd.read_excel(old_path_, sheet_name='Список заявок')

    df818old.drop(['Вид документа', 'Наименование документа', 'Статус документа', 'Дата формирования документа',
                'Текущий подписант'], axis=1, inplace=True)

    df818_stadii = pd.read_excel(save_path_3_ + r'\818.xlsx')
    df818_stadii.insert(4, 'НомерЗаявкиКороткий', df818_stadii['НомерЗаявки'].apply(lambda x: x.split('-(')[0]))
    df818_stadii = df818_stadii[df818_stadii['СтатусДокумента'] != 'отказ от подписи']
    df818_stadii.drop_duplicates(subset=['НомерЗаявки'], keep='first', inplace=True)

    df818_stadii = df818_stadii[['НомерЗаявкиКороткий', 'ВидДокумента', 'НаименованиеДокумента', 'СтатусДокумента',
                                 'ДатаФормированияДокумента', 'Подписант']]

    df818 = pd.concat([df818old, df818], ignore_index=True)
    df818['№ заявки ДГИ.1'] = df818['№ заявки ДГИ.1'].apply(lambda x: x.split('-(')[0])
    df818.drop_duplicates(subset=['№ заявки ДГИ'], keep='first', inplace=True)
    df818 = df818.merge(df818_stadii, left_on='№ заявки ДГИ.1', right_on='НомерЗаявкиКороткий', how='left')
    df818.drop_duplicates(subset=['№ заявки ДГИ'], keep='first', inplace=True)
    df818.drop(['НомерЗаявкиКороткий'], axis=1, inplace=True)

    df818 = df818[['№', 'Источник', 'Время поступления', '№ заявки ДГИ', '№ заявки ДГИ.1', 'Дата заявки ДГИ',
                   'Дата контроля', 'Вид государственной услуги', 'Заявитель', 'Почтовый адрес заявителя',
                   'Сведения о действующих отношениях, номер документа', 'План', 'Исполнитель', 'ВидДокумента',
                   'НаименованиеДокумента', 'СтатусДокумента', 'ДатаФормированияДокумента', 'Подписант',
                   'Дата распоряжения', 'Номер распоряжения', 'Родительский процесс', 'Дата окончания приостановки']]

    df818.to_excel(res_path_ + r'\spisok_zayavok.xlsx')
    att_paths.append(res_path_ + r'\spisok_zayavok.xlsx')


    # Список с сотрудниками
    workers_list_ = ['Жиганшина Галия Ильгамовна', 'Козлова Дарья Александровна', 'Парамонова Лариса Сергеевна',
                     'Понимаскина Ирина Владимировна', 'Шалепина Татьяна Анатольевна']

    df818_stadii = pd.read_excel(save_path_3_ + r'\818.xlsx')
    df818_stadii = df818_stadii[df818_stadii['СтатусДокумента'] == 'на согласовании']
    df818_stadii.drop_duplicates(subset=['НомерЗаявки'], keep='first', inplace=True)
    df818_stadii.insert(4, 'НомерЗаявкиКороткий', df818_stadii['НомерЗаявки'].apply(lambda x: x.split('-(')[0]))

    df818_stadii = df818_stadii[['Процесс', 'НомерЗаявки', 'НомерЗаявкиКороткий', 'ДатаКонтроля', 'ДатаЗаявки',
                                 'СведенияОПредставителеЗаявителя', 'ВидДокумента', 'НаименованиеДокумента',
                                 'СтатусДокумента', 'ФиоПоследнегоСогласующего', 'ДатаПоследнегоСогласования',
                                 'Подписант', 'ДатаПодписи', 'ДатаОтказа', 'ДатаФормированияДокумента',
                                 'НомерУчетногоДела', 'НомерРд', 'СуммаСубсидии']]

    df818_stadii = df818_stadii[df818_stadii['Подписант'].isin(workers_list_)]
    df818_stadii.to_excel(res_path_ + r'\othchet_po_soglam.xlsx', index=False)
    att_paths.append(res_path_ + r'\othchet_po_soglam.xlsx')

    df1004 = pd.read_excel(save_path_2_ + r'\1004.xlsx')
    df1004.to_excel(res_path_ + r'\1004_v_rabote.xlsx', index=False)
    att_paths.append(res_path_ + r'\1004_v_rabote.xlsx')

    df1004 = pd.read_excel(save_path_3_ + r'\1004.xlsx')
    df1004 = df1004[(df1004['ДатаПодписи'] >= datetime.strftime(datetime.strptime(dstart_2_, '%d.%m.%Y'), '%Y-%m-%d')) &
                    (df1004['ДатаПодписи'] <= datetime.strftime(datetime.strptime(dend_, '%d.%m.%Y'), '%Y-%m-%d'))]
    df1004.drop_duplicates(subset=['НомерЗаявки'], keep='first', inplace=True)

    df1004 = df1004[['Процесс', 'НомерЗаявки',  'ДатаКонтроля', 'ДатаЗаявки',
                                 'СведенияОПредставителеЗаявителя', 'ВидДокумента', 'НаименованиеДокумента',
                                 'СтатусДокумента', 'ФиоПоследнегоСогласующего', 'ДатаПоследнегоСогласования',
                                 'Подписант', 'ДатаПодписи', 'ДатаОтказа', 'ДатаФормированияДокумента',
                                 'НомерУчетногоДела', 'НомерРд', 'СуммаСубсидии']]

    df1004.to_excel(res_path_ + r'\1004.xlsx', index=False)
    att_paths.append(res_path_ + r'\1004.xlsx')

    login_mail = config.EMAIL_LOG
    password_mail = config.EMAIL_PASS
    server = "owa.mos.ru"
    port = 587
    recipients = [email_]
    cc = ['ArsenevVD@mos.ru']

    mail_date = datetime.strftime(datetime.today(), '%d.%m.%Y')

    subject = 'Материалы для отчета' + mail_date
    body = 'Материалы, сформированные автоматически'

    SMTPmail.send_email(login_mail, password_mail, server, port, recipients, cc, subject, body, att_paths)

    return 'Письмо успешно направлено'

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'
        }
    s = datetime.now()
    print(s)
    user = 'ArsenevVD%40mlc.gov'
    password = 'Vitosik0201.'
    # usluga = '691'
    # d_start = '01.01.2024'
    # d_end = '19.03.2024'
    # spd_ispolnenie(user, password, gosusl_='1004', spd_status_='Подано', save_path_=r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\data\likhach_report\1004')
    # time.sleep(60)
    # df_final = spd_stadii_sogl(user, password, d_start, d_end, usluga)
    # df_final = spd_ispolnenie(user, password, gosusl_='1004', spd_status_='Подано',
    #                save_path_=r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\data\likhach_report\1004')
    # df_final.to_excel(r'C:\Users\ArsenevVD\Downloads\\'+usluga+'.xlsx', index=False)
    # df = pd.read_excel(r'C:\Users\ArsenevVD\Downloads\\'+usluga+'.xlsx')
    print(likhach_report('ArsenevVD@mos.ru'))
    e = datetime.now()
    print(e)
    print()
    print('time is ', e-s)
    

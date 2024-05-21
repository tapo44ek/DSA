# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 11:35:45 2023

@author: ArsenevVD
"""

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Функция для отправки письма с вложением
def send_email(login, password, server, port, recipients, cc, subject, body, attachment_paths):
    # Создаем объект MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = 'ArsenevVD@mos.ru'
    msg['To'] = ', '.join(recipients)
    msg['Cc'] = ', '.join(cc)
    msg['Subject'] = subject

    # Добавляем текстовую часть письма
    msg.attach(MIMEText(body, 'plain'))
    
    # Открываем файл в режиме бинарного чтения
    for attachment_path in attachment_paths:
#        fname = attachment_path.split('\\')[len(attachment_path.split('\\'))-1] 
#        with open(attachment_path, 'rb') as attachment:
#            # Создаем объект MIMEBase для вложения
#            part = MIMEBase('application', 'octet-stream')
#            part.set_payload(attachment.read())
#            encoders.encode_base64(part)
#            part.add_header('Content-Disposition', f'attachment; filename= {attachment_path}')
#
#            # Прикрепляем вложение к письму
#            msg.attach(part)
        mime_type, _ = mimetypes.guess_type(attachment_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        main_type, sub_type = mime_type.split('/', 1)
        fname = str(os.path.basename(attachment_path))
        print(fname)
        with open(attachment_path, 'rb') as attachment:
            print(attachment_path)
            part = MIMEBase(main_type, sub_type)
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment', filename= fname)
            msg.attach(part)

    # Устанавливаем соединение с сервером SMTP
    with smtplib.SMTP(server, port) as server:
        server.starttls()
        server.login(login, password)

        # Отправляем письмо
        server.send_message(msg)

    print("Письмо успешно отправлено!")

# Задаем параметры для отправки письма
#login = r"HQ\ArsenevVD"
#password = "Vitosik0201?"
#server = "owa.mos.ru"
#port = 587
##recipients = ['ArsenevVD@mos.ru', 'GabitovDS@mos.ru']
#recipients = ['ArsenevVD@mos.ru']
##cc = ['FatykhovaLM@mos.ru', 'SafinRR@mos.ru']
#cc = ['GabitovDS@mos.ru']
#subject = 'Красный и предупредительный контроли'
#body = 'Данное сообщение сформировано автоматически \n \nДоброе утро! \n \nПо состоянию на ХХ.ХХ.ХХХХ за Управлением ведения жилищного учета числятся просроченные обращения в количестве: ХХ шт. \nИз них количество обращений, срок исполнения которых истек более 2 месяцев назад составляет: ХХ шт. \n \nВо избежание проблем в части нарушения исполнительской дисциплины в Управлении, прошу обратить особое внимание на данный контроль и усилить меры по исполнению и закрытию вышеуказанных обращений. \n \nВ случае наличия объективных причин для неисполнения обращения в срок, необходимо продлить контрольный срок по согласованию с начальником Управления.'
#path = 'C:\\Users\\ArsenevVD\\Desktop\\Контроль писем общий\\Контроль 06.22-07.22\\'

#attachment_paths = [path+'Красный контроль 2023-06-22.xlsx', path+'Предупредительный контроль 2023-06-22.xlsx']
#, path+'Предупредительный контроль 2023-06-22.xlsx'

# Отправляем письмо
#send_email(login, password, server, port, recipients, cc, subject, body, attachment_paths)


import time
import datetime
from datetime import datetime

import data_module
import sedo
from handlers import bot
import schedule
import asyncio


def add_task_to_schedule(interval, task_function):
    schedule.every().day.at(interval).do(task_function)


def notific(time_list_):
    notification1 = 'Привет! Напоминаю, текущее время - {time_now}'
    while True:
        time_now = datetime.now()
        time_now = datetime.strftime(time_now, '%H:%M')
        print(time_now)
        a, b = data_module.notification_search(time_now)
        if len(a) > 0:
            for item in a:
                #Вот сюда вписать инициализацию функции проверки соглов, вывод - готовое сообщение, функция из
                #sedo.py
                asyncio.run(bot.send_message(chat_id=item['TG_id'], text=sedo.sogl_update(item['Worker'].split()[0]
                                                                                          + ' ' + item['Worker'].split()[1][0]
                                                                                          + '. ' + item['Worker'].split()[2][0]
                                                                                          + '.', item['SEDO_id'])))
                asyncio.run(bot.send_message(chat_id=item['TG_id'], text='тестовое напоминание о соглах'))
                asyncio.run(bot.session.close())
        if len(b) > 0:
            for item in b:
                asyncio.run(bot.send_message(chat_id=item['TG_id'], text=item['text']))
                asyncio.run(bot.session.close())
        # if time_now in time_list_:
        #     notification = notification1.format(time_now=time_now)
        #     Bot = bot.send_message(chat_id=260399228, text=notification)
        #     asyncio.run(Bot)
        #     asyncio.run(bot.session.close())
        #     print('HEY')
        time.sleep(60)
    return



if __name__ == "__main__":
    time_list = ['15:33', '15:34', '15:35']
    notific(time_list)
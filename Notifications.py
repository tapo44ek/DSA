import time
import datetime
from datetime import datetime
import multiprocessing as mp

from aiogram import Bot
from aiogram.enums import ParseMode
import config
import data_module
from sedo import sogl_upd
# from handlers import bot
import asyncio

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
def send_not(FIO, id_tg, id_sedo):
    asyncio.run(bot.send_message(chat_id=id_tg, text=sogl_upd(FIO, id_sedo)))
    try:
        asyncio.run(bot.session.close())
    except:
        pass


def notific():

    while True:

        time_now = datetime.now()
        time_now = datetime.strftime(time_now, '%H:%M')
        print(time_now)
        a, b = data_module.notification_search(time_now)

        if len(a) > 0:

            for item in a:

                #Вот сюда вписать инициализацию функции проверки соглов, вывод - готовое сообщение, функция из
                #sedo.py
                a = item['Worker'].split()[0] + ' ' + item['Worker'].split()[1][0] + '.' + item['Worker'].split()[2][0] + '.'
                p = mp.Process(target=send_not, args=(a, item['TG_id'], item['SEDO_id']))
                p.start()


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
    notific()

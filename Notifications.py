import time
import datetime
from datetime import datetime
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
        if time_now in time_list_:
            notification = notification1.format(time_now=time_now)
            Bot = bot.send_message(chat_id=309025156, text=notification)
            asyncio.run(Bot)
            print('HEY')
        time.sleep(60)
    return



if __name__ == "__main__":
    time_list = ['15:45','15:47','15:50']
    notific(time_list)
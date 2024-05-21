import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import handlers
import config
import subprocess
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a", format="%(asctime)s %(levelname)s %(message)s")
    # subprocess.Popen(['python', 'Notifications.py'])
    asyncio.run(main())
    # exec(open('Notifications.py').read())

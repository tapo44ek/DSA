
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
import config
import data_module
import kb
import text
import re
router = Router()
# bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

# @router.message(Command("start"))
# async def start_handler(msg: Message):
#     await bot.send_message(1944422362, "Привет")

# @router.message(F.text == "Меню")
# @router.message(F.text == "Выйти в меню")
# @router.message(F.text == "◀️ Выйти в меню")
# async def menu(msg: Message):
#     await msg.answer(text.menu, reply_markup=kb.menu)


# @router.message(F.text == 'Кто я')
# @router.message(F.text == 'кто я')
# @router.message(F.text == 'Whoami')
# @router.message(F.text == 'whoami')
# async def start_handler(msg: Message):
#     await msg.answer(str(data_module.whoami(msg.from_user.id)))
@router.message(F.text == 'Арсеньев')
async def start_handler(msg: Message):
    await msg.answer('Это мой создатель')
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await msg.answer(str(data_module.search(msg.text, msg.from_user.id)))


@router.message(F.text)
async def start_handler(msg: Message):
    print(msg.text)
    # result = data_module.search(msg.text, msg.from_user.id)
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await msg.answer(str(data_module.search(msg.text, msg.from_user.id)))




from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
import config
import data_module
import kb
import text
import re
router = Router()


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



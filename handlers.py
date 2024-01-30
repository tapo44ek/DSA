
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from main import bot
import config
import data_module
import kb
import text
import re
router = Router()


class UserActions(StatesGroup):
    actions = State()
    menu = State()
    phone_helper = State()
    settings = State()
    base_change = State()


# bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

@router.message(Command("start"))
async def start_handler(msg: Message):
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await bot.send_message(msg.from_user.id, "Привет")




@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message, state: FSMContext):
    await msg.answer(text.menu, reply_markup=kb.menu)
    await state.set_state(UserActions.menu)

# @router.message(F.text == 'Кто я')
# @router.message(F.text == 'кто я')
# @router.message(F.text == 'Whoami')
# @router.message(F.text == 'whoami')
# async def start_handler(msg: Message):
#     await msg.answer(str(data_module.whoami(msg.from_user.id)))


@router.callback_query(F.data == "/menu")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.menu, reply_markup=kb.menu)
    await state.set_state(UserActions.menu)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.callback_query(F.data == "/phone_helper")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.phone_helper_main, reply_markup=kb.iexit_kb)
    await state.set_state(UserActions.phone_helper)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.callback_query(F.data == "/sedo")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.no_code, reply_markup=kb.iexit_kb)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.message(UserActions.phone_helper, F.text == 'Арсеньев')
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer('Это мой создатель')
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await msg.answer(str(data_module.search(msg.text, msg.from_user.id)), reply_markup=kb.iexit_kb)
    await state.set_state(UserActions.phone_helper)


@router.message(UserActions.phone_helper, F.text)
async def start_handler(msg: Message, state: FSMContext):
    print(msg.text)
    # result = data_module.search(msg.text, msg.from_user.id)
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await msg.answer(str(data_module.search(msg.text, msg.from_user.id)), reply_markup=kb.iexit_kb)
    await state.set_state(UserActions.phone_helper)


@router.message(F.text == "отправь сообщение")
async def menu(bot: bot):
    await bot.send_message(chat_id=309025156, text='<b>напиши мне что-нибудь</b>')


@router.callback_query(F.data == "/settings")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    print(callback.from_user.id)
    print(data_module.check_admin(callback.from_user.id))
    await state.set_state(UserActions.settings)
    await callback.message.answer(text.settings, reply_markup=kb.settings)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.callback_query(F.data == "/base_change")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserActions.base_change)
    await callback.message.answer(text.upd_text, reply_markup=kb.iexit_kb)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.message(UserActions.base_change, F.text)
async def start_handler(msg: Message):
    print(msg.text)
    data = msg.text.split('::')
    cols = data[1].split(', ')
    print(cols)
    vals = data[2].split(', ')
    print(vals)
    # result = data_module.search(msg.text, msg.from_user.id)
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await msg.answer(str(data_module.update_table(data[0], cols, vals, data[3], data[4], msg.from_user.id)), reply_markup=kb.iexit_kb)


@router.message(F.text)
async def unknown_msg(msg: Message):
    await msg.answer(text.unknown_msg, reply_markup=kb.iexit_kb)

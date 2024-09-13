import os
import sys
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from main import bot
import sedo
import data_module
import kb
import text
import subprocess
import SPD2_download
import likhach_report
import multiprocessing as mp
from Notifications import force_notific

router = Router()


class UserActions(StatesGroup):
    actions = State()
    menu = State()
    phone_helper = State()
    settings = State()
    base_change = State()
    notification_set = State()
    SPD2_type = State()
    SPD2_dstart = State()
    SPD2_dend = State()
    SPD2_dub = State()
    SPD2_add = State()
    SPD2_text = State()
    last_menu_message_id = State()
# bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)


@router.message(CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject):
    data_module.chat_checker(message.from_user.id, message.chat.id)
    args = command.args
    payload = decode_payload(args)
    await message.answer(f"Your payload: {payload}")


@router.message(Command("start"))
async def start_handler(msg: Message):
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await bot.send_message(msg.from_user.id, "Привет")


@router.message(Command("menu"))
@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message, state: FSMContext):
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    role = data_module.check_admin(msg.from_user.id)
    if role == 2:
        await msg.answer(text.menu, reply_markup=kb.menu_ruk)
    else:
        await msg.answer(text.menu, reply_markup=kb.menu)
    await state.set_state(UserActions.menu)



@router.callback_query(F.data == "/menu")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    role = data_module.check_admin(callback.from_user.id)
    if role == 2:
        await callback.message.answer(text.menu, reply_markup=kb.menu_ruk)
    else:
        await callback.message.answer(text.menu, reply_markup=kb.menu)
    # await callback.message.delete()
    await state.set_state(UserActions.menu)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.callback_query(F.data == "/force_update")
async def force_update(callback: types.CallbackQuery, state: FSMContext):
    role = data_module.check_admin(callback.from_user.id)
    await callback.message.answer('Обновление запущено, ожидайте ответ в течение пары минут', reply_markup=kb.iexit_kb)
    # await callback.message.delete()
    await callback.answer(
        text="Успешно",
        show_alert=False
    )
    p = mp.Process(target=force_notific, args=(callback.from_user.id,), )
    p.start()


@router.callback_query(F.data == "/phone_helper")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer(text.phone_helper_main, reply_markup=kb.iexit_kb)
    await state.set_state(UserActions.phone_helper)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.callback_query(F.data == "/notification_times")
async def set_notifications(callback: types.CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer(text.notifications_settings_1.format(
        notifics_=data_module.get_notification(callback.from_user.id)
        ), reply_markup=kb.settings_notifics)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.callback_query(F.data == "/set_notifications")
async def set_notifications(callback: types.CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer(text.notifications_settings_2, reply_markup=kb.iexit_kb)
    await state.set_state(UserActions.notification_set)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.message(UserActions.notification_set)
async def start_handler(msg: Message):
    await bot.send_message(chat_id=msg.from_user.id,
                           text=data_module.set_notification(msg.from_user.id, msg.text),
                           reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "/report_brg_moa")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    if data_module.check_admin(callback.from_user.id) == 1:
        # await callback.message.delete()
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Выгрузка запущена, примерное время ожидания 2-4 минуты',
                               reply_markup=kb.iexit_kb)
        await callback.answer(
            text="Успешно",
            show_alert=False
        )
        # await callback.message.answer(text=sedo.sogl_report_send(data_module.get_email(callback.from_user.id)),
        #                               reply_markup=kb.iexit_kb)
        # p = mp.Process(target=sedo.sogl_report_send, args=(data_module.get_email(callback.from_user.id),), )
        # p.start()
        p = mp.Process(target=sedo.sogl_report_send, args=(callback.from_user.id,), )
        p.start()

    else:
        # await callback.message.delete()
        await callback.message.answer(text.no_code, reply_markup=kb.iexit_kb)
        await callback.answer(
            text="Успешно",
            show_alert=False
        )


@router.callback_query(F.data == "/sedo")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    print(data_module.check_admin(callback.from_user.id))
    if data_module.check_admin(callback.from_user.id) == 1:
        await callback.message.answer(text='Меню взаимодействия с СЭДО', reply_markup=kb.sedo_adm_kb)
        # await callback.message.delete()
    else:
        await callback.message.answer(text.no_code, reply_markup=kb.iexit_kb)
        # await callback.message.delete()
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.callback_query(F.data == "/spd")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    # print(data_module.check_admin(callback.from_user.id))
    # if data_module.check_admin(callback.from_user.id) == 1:
    #     await callback.message.answer(text='Меню взаимодействия с СЭДО', reply_markup=kb.sedo_adm_kb)
    # else:
    #     await callback.message.answer(text.no_code, reply_markup=kb.iexit_kb)
    # await callback.message.delete()
    await callback.message.answer(text='Меню взаимодействия с СПД', reply_markup=kb.spd_kb)

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
    role = data_module.check_admin(callback.from_user.id)
    if role == 1:
        await callback.message.answer(text.settings, reply_markup=kb.settings_adm)
    else:
        await callback.message.answer(text.settings, reply_markup=kb.settings)
    await state.set_state(UserActions.menu)

    await state.set_state(UserActions.settings)
    # await callback.message.delete()
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.callback_query(F.data == "/base_change")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserActions.base_change)
    # await callback.message.delete()
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
    await msg.answer(str(data_module.update_table(data[0], cols, vals, data[3], data[4], msg.from_user.id)),
                     reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "/start_red_control")
async def red_control(callback: types.CallbackQuery):
    # await callback.message.delete()
    await callback.message.answer("Запускаю Красный и предупредительный контроль\nОжидайте минут 15 и проверьте почту",
                                  reply_markup=kb.iexit_kb)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )
    data_module.set_report('red_control', callback.from_user.id)
    python_exec = os.path.join(sys.prefix, 'bin', 'python')
    # subprocess.call('Notifications.py', env=current_env)
    subprocess.Popen([python_exec, 'red_control.py'])
    # proc = subprocess.Popen([r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\venv\Scripts\python',
    #                          r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\red_control.py'])


@router.callback_query(F.data == "/start_control_mail")
async def red_control(callback: types.CallbackQuery):
    # await callback.message.delete()
    await callback.message.answer("Контроль писем запущен\nОжидайте минут 20 и проверьте почту",
                                  reply_markup=kb.iexit_kb)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )
    data_module.set_report('control_mail', callback.from_user.id)
    python_exec = os.path.join(sys.prefix, 'bin', 'python')
    # subprocess.call('Notifications.py', env=current_env)
    subprocess.Popen([python_exec, 'part2.py'])
    # proc = subprocess.Popen([r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\venv\Scripts\python',
                             # r'C:\Users\ArsenevVD\Desktop\control_mail_2.1\DSA-main\part2.py'])


# @router.callback_query(F.data == "/spd_2")
# async def helper_status(callback: types.CallbackQuery, state: FSMContext):
#     print(callback.from_user.id)
#     print(data_module.check_admin(callback.from_user.id))
#     await state.set_state(UserActions.SPD2_type)
#     await callback.message.answer('Введите тип фильрации', reply_markup=kb.settings)
#     await callback.answer(
#         text="Успешно",
#         show_alert=False
#     )


@router.callback_query(F.data == "/spd_2")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    print(callback.from_user.id)
    print(data_module.check_admin(callback.from_user.id))
    await state.set_state(UserActions.SPD2_type)
    await callback.message.answer('Введите тип фильрации', reply_markup=kb.spd_2_type)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.callback_query(F.data, UserActions.SPD2_type)
async def spd_2(callback: types.CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer("Введите дату начала отчетного периода в формате 'ДД.ММ.ГГГГ', (пример - 01.01.2024)",
                                  reply_markup=kb.iexit_kb)
    await state.update_data(SPD2_type=int(callback.data))
    a = await state.get_data()
    print(a['SPD2_type'])
    await state.set_state(UserActions.SPD2_dstart)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.message(F.text, UserActions.SPD2_dstart)
async def spd_2(msg: Message, state: FSMContext):
    await state.update_data(SPD2_dstart=msg.text)
    a = await state.get_data()
    print(a['SPD2_type'])
    print(a['SPD2_dstart'])

    await msg.answer("Введите дату конца отчетного периода в формате 'ДД.ММ.ГГГГ', (пример - 01.01.2024)",
                                  reply_markup=kb.iexit_kb)
    await state.set_state(UserActions.SPD2_dend)


@router.message(F.text, UserActions.SPD2_dend)
async def spd_2(msg: Message, state: FSMContext):
    await state.update_data(SPD2_dend=msg.text)
    a = await state.get_data()
    print(a['SPD2_type'])
    print(a['SPD2_dstart'])
    print(a['SPD2_dend'])
    await msg.answer("Нужны ли Вам приостановки?",
                                  reply_markup=kb.spd_2_dub)
    await state.set_state(UserActions.SPD2_dub)


@router.callback_query(F.data, UserActions.SPD2_dub)
async def spd_2(callback: types.CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer("Добавить выгрузку текстов документов?\n----\nВНИМАНИЕ\nВЫГРУЗКА ЗАЙМЕТ ГОРАЗДО БОЛЬШЕ ВРЕМЕНИ",
                                  reply_markup=kb.spd_2_text)
    await state.update_data(SPD2_dub=int(callback.data))
    a = await state.get_data()
    print(a['SPD2_dub'])
    await state.set_state(UserActions.SPD2_text)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


@router.callback_query(F.data, UserActions.SPD2_text)
async def spd_2(callback: types.CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer("Выгрузка запущена, ожидайте письмо на почте через 5-10 минут",
                                  reply_markup=kb.iexit_kb)

    await state.update_data(SPD2_text=int(callback.data))
    a = await state.get_data()
    print(a['SPD2_type'])
    await state.clear()
    p = mp.Process(target=SPD2_download.spd_2_download, args=(data_module.get_email(callback.from_user.id),
                                                              a['SPD2_dstart'], a['SPD2_dend'], a['SPD2_type'],
                                                              a['SPD2_dub'], a['SPD2_text'], callback.from_user.id),)
    p.start()
    await callback.answer(
        text="Успешно",
        show_alert=False
    )


# @router.callback_query(F.data, UserActions.SPD2_type)
# async def spd_2(callback: types.CallbackQuery):
#     await callback.message.answer("Выгрузка запущена, ожидайте письмо на почте через 5-10 минут",
#                                   reply_markup=kb.iexit_kb)
#     await callback.answer(
#         text="Успешно",
#         show_alert=False
#     )
#     # await callback.message.answer(text=SPD2_download.spd_2_download(data_module.get_email(callback.from_user.id)),
#     #                               reply_markup=kb.iexit_kb)
#     p = mp.Process(target=SPD2_download.spd_2_download, args=(data_module.get_email(callback.from_user.id), ),)
#     p.start()


@router.callback_query(F.data == "/report_likhach")
async def report_likhach(callback: types.CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Выгрузка запущена, примерное время ожидания 5-15 минут',
                           reply_markup=kb.iexit_kb)
    await callback.answer(
        text="Успешно",
        show_alert=False
    )
    # await callback.message.answer(text=likhach_report.likhach_report(data_module.get_email(callback.from_user.id)),
    #                               reply_markup=kb.iexit_kb)
    p = mp.Process(target=likhach_report.likhach_report, args=(data_module.get_email(callback.from_user.id), ),)
    p.start()
    # await callback.message.answer(text=likhach_report.likhach_report(data_module.get_email(callback.from_user.id)),
    #                               reply_markup=kb.iexit_kb)
    # if data_module.check_admin(callback.from_user.id) == 1:
    #     await bot.send_message(chat_id=callback.from_user.id,
    #                            text='Выгрузка запущена, примерное время ожидания 5-15 минут',
    #                            reply_markup=kb.iexit_kb)
    #     await callback.answer(
    #         text="Успешно",
    #         show_alert=False
    #     )
    #     await callback.message.answer(text=likhach_report.likhach_report(data_module.get_email(callback.from_user.id)),
    #                                   reply_markup=kb.iexit_kb)
    #
    #
    # else:
    #     await callback.message.answer(text.no_code, reply_markup=kb.iexit_kb)
    #     await callback.answer(
    #         text="Успешно",
    #         show_alert=False
    #     )


@router.message(F.text)
async def unknown_msg(msg: Message):
    await msg.answer(text.unknown_msg, reply_markup=kb.iexit_kb)

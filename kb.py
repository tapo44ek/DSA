from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="📝 СЭДО", callback_data="/sedo")],
    [InlineKeyboardButton(text="🔎 Телефонный справочник", callback_data="/phone_helper")],
    [InlineKeyboardButton(text="💳 Настройки", callback_data="/settings")]
]
settings = [
    [InlineKeyboardButton(text="📝 Внести изменения в базу", callback_data="/base_change")],
    [InlineKeyboardButton(text="📝 Посмотреть напоминания", callback_data="/notification_times")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="/menu")]
]

settings_notifics = [
    [InlineKeyboardButton(text="📝 Изменить время", callback_data="/set_notifications")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="/menu")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
settings = InlineKeyboardMarkup(inline_keyboard=settings)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню",
                                                                       callback_data="/menu")]])
sedo_adm_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отчет по соглам БРГ и МОА",
                                                                          callback_data="/report_brg_moa")],
                                                    [InlineKeyboardButton(text="Красный контроль",
                                                                          callback_data="/start_red_control")],
                                                    [InlineKeyboardButton(text="Контроль писем",
                                                                          callback_data="/start_control_mail")],
                                                    [InlineKeyboardButton(text="Выгрузка СПД-2",
                                                                          callback_data="/spd_2_download")],
                                                    [InlineKeyboardButton(text="◀️ Выйти в меню",
                                                                          callback_data="/menu")]])

settings_notifics = InlineKeyboardMarkup(inline_keyboard=settings_notifics)

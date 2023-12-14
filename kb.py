from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="📝 СЭДО", callback_data="/sedo")],
    [InlineKeyboardButton(text="🔎 Телефонный справочник", callback_data="/phone_helper")],
    [InlineKeyboardButton(text="💳 Настройки", callback_data="/settings")]
]
settings = [
    [InlineKeyboardButton(text="📝 Внести изменения в базу", callback_data="/base_change")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="/menu")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
settings = InlineKeyboardMarkup(inline_keyboard=settings)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="/menu")]])
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


botInlineKbd = InlineKeyboardMarkup()
botInlineKbd.row(InlineKeyboardButton(text="Статистика", callback_data="stats"),
                         InlineKeyboardButton(text="Топ стран", callback_data="topCountry"))
botInlineKbd.row(InlineKeyboardButton(text="Топ 20 турниров", callback_data="top20Tourney"))
botInlineKbd.row(InlineKeyboardButton(text="Топ 50 турниров", callback_data="top50Tourney"))

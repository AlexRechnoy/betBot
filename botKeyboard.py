from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


botStatsKbd = InlineKeyboardMarkup()
botStatsKbd.row(InlineKeyboardButton(text="Cуммарная статистика", callback_data="stats"))

botAdditionalStatsKbd = InlineKeyboardMarkup()
botAdditionalStatsKbd.row(InlineKeyboardButton(text="Топ стран", callback_data="topCountry"))
botAdditionalStatsKbd.row(InlineKeyboardButton(text="Топ 20 турниров", callback_data="top20Tourney"),
                          InlineKeyboardButton(text="Топ 50 турниров", callback_data="top50Tourney"))

botOnlineStatsKbd = InlineKeyboardMarkup()
botOnlineStatsKbd.row(InlineKeyboardButton(text="Статистика по текущим матчам", callback_data="onlineStats"))

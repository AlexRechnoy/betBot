from aiogram import Dispatcher
from bot_data import botData
from botKeyboard import botOnlineStatsKbd
from datetime import datetime

myChatID = 1082319898

async def get_online_matches(dp: Dispatcher):
    #onlineGamesData,gameCount=botData.getOnlineFlashScoreGames()
    onlineGamesData, gameCount = botData.getOnline1XstavkaGames()
    if gameCount>0:
        await dp.bot.send_message(myChatID, onlineGamesData, parse_mode="Markdown", reply_markup=botOnlineStatsKbd)

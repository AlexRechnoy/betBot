from aiogram import Dispatcher
from betData import BetData
from botKeyboard import botInlineKbd
from datetime import datetime

myChatID = 1082319898


async def get_online_matches(dp: Dispatcher, betData: BetData):
    onlineGamesData,gameCount=betData.getOnlimeGames()
    print(datetime.now().strftime('%H:%M'))
    if gameCount>0:
        await dp.bot.send_message(myChatID, onlineGamesData, parse_mode="Markdown", reply_markup=botInlineKbd)

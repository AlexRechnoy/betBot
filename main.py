from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from botKeyboard import botInlineKbd
from betData import BetData
from botTimer import get_online_matches
from botCommands import cmd_help,myfunc
import config
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('endproc', nargs='?')
    return parser

bot = Bot(token=config.BOT_TOKEN)
betData=BetData()
dp = Dispatcher(bot)

myfunc('sd',args=(5,15),mybetData=betData, check='ddd')

#
dp.register_message_handler(cmd_help, custom_filters=(None), commands="help")
#
scheduler = AsyncIOScheduler()
scheduler.add_job(get_online_matches, "interval", seconds=5, args=(dp,betData))


@dp.callback_query_handler(text="stats")
async def cmd_top10C(call: types.CallbackQuery):
    await call.message.answer(betData.getStats(), parse_mode="Markdown",reply_markup=botInlineKbd)
    await call.answer()

@dp.callback_query_handler(text="topCountry")
async def cmd_top10C(call: types.CallbackQuery):
    await call.message.answer(betData.getTopCountries(10), parse_mode="Markdown",reply_markup=botInlineKbd)
    await call.answer()

@dp.callback_query_handler(text="top20Tourney")
async def cmd_top20T(call: types.CallbackQuery):
    await call.message.answer(betData.getTopTourneys(20), parse_mode="Markdown",reply_markup=botInlineKbd)
    await call.answer()

@dp.callback_query_handler(text="top50Tourney")
async def cmd_top50T(call: types.CallbackQuery):
    await call.message.answer(betData.getTopTourneys(50), parse_mode="Markdown",reply_markup=botInlineKbd)
    await call.answer()

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.from_user.id,betData.getCountryStats(message.text),parse_mode="Markdown")
    await message.answer("Дополнительная статистика :  ", reply_markup=botInlineKbd)

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    #print(betData.getOnlimeGames())
    if not namespace.endproc:
        scheduler.start()
        executor.start_polling(dp, skip_updates=True)
from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from botKeyboard import botInlineKbd
from betData import BetData
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
dp.register_message_handler(cmd_help, custom_filters=(None), commands="help", regexp=None, content_types=None,
                                 state=None, run_task=None)
#dp.register_message_handler(cmd_top10C, commands="top10C",myBetData=betData, myBotData=bot)

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

    #print(betData.getTopCountries(10))
    #rint(betData.getTopTourneys(20))
    if not namespace.endproc:
        #scheduler.start()
        executor.start_polling(dp, skip_updates=True)
from aiogram import Bot,types,dispatcher
from botKeyboard import botAdditionalStatsKbd,botStatsKbd
from bot_data import botData
from  botDispatcher import bot

async def cmd_help(message: types.Message):
    await message.reply('*Я помогу в статистике турниров! \n*'
                        'Чтобы получить статистику по стране напиши мне ее название!',
                         parse_mode='Markdown')

async def callback_stats(call: types.CallbackQuery):
    await call.message.answer(botData.getStats(), parse_mode="Markdown",reply_markup=botAdditionalStatsKbd)
    await call.answer()

async def callback_online_stats(call: types.CallbackQuery):
    countryList=botData.getOnlineStats()
    if len(countryList)>0:
        for countryStr in countryList:
            if len(countryStr)<4000 :
                await call.message.answer(countryStr, parse_mode="Markdown")
    await call.answer()

async def callback_top10C(call: types.CallbackQuery):
    await call.message.answer(botData.getTopCountries(10), parse_mode="Markdown",reply_markup=botStatsKbd)
    await call.answer()

async def callback_top20T(call: types.CallbackQuery):
    await call.message.answer(botData.getTopTourneys(20), parse_mode="Markdown",reply_markup=botStatsKbd)
    await call.answer()

async def callback_top50T(call: types.CallbackQuery):
    await call.message.answer(botData.getTopTourneys(50), parse_mode="Markdown",reply_markup=botStatsKbd)
    await call.answer()

async def message_any(message: types.Message):
    await bot.send_message(message.from_user.id,botData.getCountryStats(message.text),parse_mode="Markdown",reply_markup=botStatsKbd)

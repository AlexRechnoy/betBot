from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from betData import BetData
import config
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('endproc', nargs='?')
    return parser

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)
scheduler=AsyncIOScheduler()

@dp.message_handler()#Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message):
    await bot.send_message(message.from_user.id,betData.getCountryStats(message.text),parse_mode="Markdown")

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    betData=BetData()
    #betData.getCountryStats('бурк')
    if not namespace.endproc:
        scheduler.start()
        executor.start_polling(dp, skip_updates=True)
from aiogram import Bot,types
from betData import BetData


def  myfunc(s,*args, test=10, **kwargs):
    print(test)
    for key,value in kwargs.items():
        print(key,'   ',value)


async def cmd_help(message: types.Message):
    await message.reply('*Я могу ответить на следующие команды:\n*'
                        '/top10C (топ 10 стран)\n'
                        '/top20T (топ 20 турниров)\n'
                        '/top50T (топ 50 турниров)\n',
                         parse_mode='Markdown')

async def cmd_top10C(message: types.Message):
    await message.reply('*Я могу ответить на следующие команды:\n*'
                        '/top10C (топ 10 стран)\n'
                        '/top20T (топ 20 турниров)\n'
                        '/top50T (топ 50 турниров)\n',
                        parse_mode='Markdown')
#await bot.send_message(message.from_user.id, betData.getTopCountries(10), parse_mode="Markdown")
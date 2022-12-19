from aiogram import Bot,types
from betData import BetData


def  myfunc(s,*args, test=10, **kwargs):
    print(test)
    for key,value in kwargs.items():
        print(key,'   ',value)


async def cmd_help(message: types.Message):
    await message.reply('*Я помогу в статистике турниров! \n*'
                        'Чтобы получить статистику по стране напиши мне ее название!',
                         parse_mode='Markdown')

import config
from aiogram import Bot, Dispatcher

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)
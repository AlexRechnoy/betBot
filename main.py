from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from botDispatcher import dp
from botTimer import get_online_matches
from botCommands import cmd_help,callback_stats,callback_online_stats,callback_top10C,callback_top20T,callback_top50T,\
                        message_any
from bot_data import botData
import argparse



def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('endproc', nargs='?')
    return parser
#
dp.register_message_handler(cmd_help, custom_filters=(None), commands="help")
dp.register_callback_query_handler(callback_stats, text="stats")
dp.register_callback_query_handler(callback_online_stats, text="onlineStats")
dp.register_callback_query_handler(callback_top10C, text="topCountry")
dp.register_callback_query_handler(callback_top20T, text="top20Tourney")
dp.register_callback_query_handler(callback_top50T, text="top50Tourney")
dp.register_message_handler(message_any)
#по таймеру :
scheduler = AsyncIOScheduler()
scheduler.add_job(get_online_matches, "interval", minutes =5, args=[dp])


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    #botData.getOnline1XstavkaGames()
    #onlineGamesData, gameCount = botData.getOnlineFlashScoreGames()
    if not namespace.endproc:
        scheduler.start()
        executor.start_polling(dp, skip_updates=True)
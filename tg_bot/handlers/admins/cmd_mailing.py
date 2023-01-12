from aiogram import types, Dispatcher, Bot

from tg_bot.services.db_api.database import Database
from tg_bot.config import load_config

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

async def cmd_mailing(msg: types.Message):
    if msg.from_user.id == 639381396:
        text = "Hello, Dear User 👋\n" \
               "\n" \
               "We made some updates for bot, so please press /start\n" \
               "\n" \
               "I can see the number of bot users growing\n" \
               "What motivates us not to stop there 🔥\n" \
               "\n" \
               "I hope you like and enjoy the bot \n" \
               "\n" \
               "Also in the last update we added the /feedback command, now you can rate the bot and our team will definitely read everything \n" \
               "\n" \
               "Thanks a lot ❤️ and enjoy!"    

        for chat_id in await Database.get_all_user_id():
            await bot.send_message(chat_id=chat_id, text=text)
    else:
        print("error")


def register_mailing(dp: Dispatcher):
    dp.register_message_handler(cmd_mailing, commands=["mailing"])
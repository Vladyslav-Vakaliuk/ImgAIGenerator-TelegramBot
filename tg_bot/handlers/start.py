from aiogram import types, Dispatcher

from tg_bot.services.db_api.database import add_user_to_db

from tg_bot.services.db_api.database import User, SessionMaker


async def cmd_start(msg: types.Message):
    first_name = msg.from_user.first_name
    text = f"Hey 👋, <b>{first_name}</b>\n" \
            "\n" \
            "I am an AI image generator bot 🤖, I can generate images from text\n" \
            "\n" \
            "To generate image press /generate\n" \
            "\n" \
            "If you need help press /help\n" \
            "\n" \
            "Developed by <a href='https://t.me/vakal33'>Vakal</a>"  
            
    await msg.answer(text=text, disable_web_page_preview=True, parse_mode="HTML")
    await add_user_to_db(user_id=msg.from_user.id, user_name=msg.from_user.first_name, user_surname=msg.from_user.last_name, username=msg.from_user.username, language=msg.from_user.language_code)
    
def register_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
from aiogram import types, Dispatcher

async def cmd_help(msg: types.Message):
    text = "<b>- How it works:</b>\n" \
           "\n" \
           "<b>- Press /generate</b>\n" \
           "\n" \
           "<b>- Write what do you want to draw</b>\n" \
           "\n" \
           "<b>- Example:</b> <code>an astronaut riding a horse on mars artstation, hd, dramatic lighting, detailed</code>\n" \
           "\n" \
           "<b>- Then after 10 - 60 seconds you will get your image</b>\n" \
           "\n" \
           "————————————————————— \n" \
           "\n" \
           "Perhaps at first you will not get the result you expect In this case, try experimenting with your text\n" \
           "\n" \
           "Since the bot works with openai api, you should familiarize yourself with their <a href='https://labs.openai.com/policies/content-policy'>content policy</a> and content that is prohibited to generate\n" \
           "\n" \
           "If you have any problems/questions/advices <a href='https://t.me/vakal33'>Contact me</a>"      

    
    await msg.answer(text=text, disable_web_page_preview=True, parse_mode="HTML")

def register_help(dp: Dispatcher):
    dp.register_message_handler(cmd_help, commands=["help"])
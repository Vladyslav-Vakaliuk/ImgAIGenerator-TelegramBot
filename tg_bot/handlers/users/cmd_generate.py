from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from tg_bot.misc.states import Generate

from tg_bot.services.openai.generate import generate_image
from tg_bot.services.db_api.database import Database
from tg_bot.keyboards.reply.cancel_btn import cancel_btn
from tg_bot.keyboards.reply.generate_btn import generate_btn

async def cmd_generate(msg: types.Message, state=None):
    text = "Now write what do you want to draw:"

    await msg.answer(text=text,reply_markup=cancel_btn(), parse_mode="HTML")

    await Generate.wait_prompt.set()


async def func_generate(msg: types.Message, state: FSMContext):
    if msg.text == "Cancel":
        await msg.answer("Canceled generating!", reply_markup=generate_btn())
        await state.finish()
    else:
        prompt = msg.text
        caption = "\n \n<span class='tg-spoiler'>Genereted with: @imgaigeneratorbot</span>"

        await msg.answer("Please wait, generating your image...")
    
        with open(await generate_image(prompt=prompt), "rb") as image:
            await msg.answer_photo(photo=image, caption=caption, reply_markup=generate_btn())
            await Database.save_prompt_to_database(user_id=msg.from_user.id, username=msg.from_user.username, prompt=msg.text, img_name=str(image))

        await state.finish()

def register_generate(dp: Dispatcher):
    dp.register_message_handler(cmd_generate, commands=["generate"])
    dp.register_message_handler(func_generate, state=Generate.wait_prompt)
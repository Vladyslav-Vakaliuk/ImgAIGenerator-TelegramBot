from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from tg_bot.misc.states import Generate

from tg_bot.services.openai.generate import generate_image

async def cmd_generate(msg: types.Message, state=None):
    text = "Now write what do you want to draw:"

    await msg.answer(text=text, parse_mode="HTML")

    await Generate.wait_prompt.set()


async def func_generate(msg: types.Message, state: FSMContext):
    prompt = msg.text
    caption = "\n \n<span class='tg-spoiler'>Genereted with: @imgaigeneratorbot</span>"

    await msg.answer("Please wait, generating your image...")

    with open(await generate_image(prompt=prompt), "rb") as image:
        await msg.answer_photo(photo=image, caption=caption)

    await state.finish()

def register_generate(dp: Dispatcher):
    dp.register_message_handler(cmd_generate, commands=["generate"])
    dp.register_message_handler(func_generate, state=Generate.wait_prompt)
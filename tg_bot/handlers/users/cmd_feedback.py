from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg_bot.misc.states import Feedback
from tg_bot.services.db_api.database import Database
from tg_bot.keyboards.reply.cancel_btn import cancel_btn
from tg_bot.keyboards.reply.generate_btn import generate_btn

async def cmd_feedback(msg: types.Message, state=None):
    text = "Here you can write your reviews/recommendations about this bot\n" \
           "\n" \
           "<b>If you don't want to do this, click Cancel!</b>\n" \
           "\n" \
           "We really appreciate it and it can help in the development of the bot \n" \
           "\n" \
           "If you are ready to write a review, you can do so immediately after this message\n" \
           "\n" \
           "Please describe your impressions of the bot, how accurately it generates images, and how it can be improved\n" \
           "\n" \
           "Thanks!)"     

    await msg.answer(text, reply_markup=cancel_btn(), parse_mode="HTML")

    await Feedback.save_feedback.set()


async def save_feedback(msg: types.Message, state: FSMContext):
    if msg.text == "Cancel":
        text = "OK, back again when will be ready )"

        await msg.answer(text, reply_markup=generate_btn())
        await state.finish()
    else:
        text = "Thank you for your feedback, we really appreciate it"
        await msg.answer(text, reply_markup=generate_btn())
        
        await Database.save_feedback(user_id=msg.from_user.id, username=msg.from_user.username, review=msg.text)
        await state.finish()

def register_feedback(dp: Dispatcher):
    dp.register_message_handler(cmd_feedback, commands=["feedback"])
    dp.register_message_handler(save_feedback, state=Feedback.save_feedback)
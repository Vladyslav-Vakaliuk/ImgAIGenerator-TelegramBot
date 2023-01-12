from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Reply button for Cancel command
def cancel_btn():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cancel = KeyboardButton("Cancel")
    kb.add(btn_cancel)
    return kb
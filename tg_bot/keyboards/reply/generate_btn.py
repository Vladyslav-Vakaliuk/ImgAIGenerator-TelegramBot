from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Reply button for /generate command
def generate_btn():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_generate = KeyboardButton("/generate")
    kb.add(btn_generate)
    return kb
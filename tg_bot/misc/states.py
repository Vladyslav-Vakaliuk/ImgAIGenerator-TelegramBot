from aiogram.dispatcher.filters.state import StatesGroup, State

class Generate(StatesGroup):
    cmd_generate = State()
    wait_prompt = State()
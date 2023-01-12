from aiogram import types, Dispatcher

async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start bot"),
        types.BotCommand("help", "Get help"),
        types.BotCommand("generate", "Generate image"), 
        types.BotCommand("feedback", "Write feedback")
    ])
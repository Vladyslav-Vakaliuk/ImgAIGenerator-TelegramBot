import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tg_bot.config import load_config
from tg_bot.models.set_my_commands import set_default_commands
from tg_bot.handlers.start import register_start
from tg_bot.handlers.help import register_help
from tg_bot.handlers.generate import register_generate
from tg_bot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)
config = load_config(".env")

storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage() # Use Redis if in file .env USE_REDIS=True else use MemoryStorage

def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config)) 
 

def register_all_filters(dp):
    pass


def register_all_handlers(dp):
    register_start(dp)
    register_help(dp)
    register_generate(dp)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        filename="logger.log"
    )

    logger.info("Starting bot")
    print("[INFO] Starting Bot")
    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
        await set_default_commands(dp)
    except:
        logger.error("Something get wrong!")
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
        print("[INFO] Bot stopped")
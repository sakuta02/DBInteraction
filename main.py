from environs import Env
import asyncio
import atexit
from packages.handlers import DBInteraction, rt
from aiogram import Bot, Dispatcher


env_instance = Env()
env_instance.read_env()
token = env_instance("Token")
bot: Bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher()
dp.include_router(rt)


async def run_bot(bot_instance: bot):
    await dp.start_polling(bot_instance, polling_timeout=20)


def cleanup():
    DBInteraction.conn.close()


if __name__ == '__main__':
    atexit.register(cleanup)
    asyncio.run(run_bot(bot))

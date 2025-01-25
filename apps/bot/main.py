import asyncio
import sys
from pathlib import Path

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage


# from apps.bot.handler.start import main_router

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")  # Loyiha nomini o'rnating
django.setup()
from apps.bot.webhook import logger
from root.settings import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN,)
storage = MemoryStorage()
async def main():
    dp = Dispatcher(storage=storage)
    from apps.bot.handler import private_handler_router
    dp.include_router(private_handler_router)
    logger.info("Bot polling orqali ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

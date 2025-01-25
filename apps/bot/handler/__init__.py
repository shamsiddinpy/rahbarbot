from aiogram import Router

from apps.bot.handler.start import main_router

private_handler_router = Router()
private_handler_router.include_router(main_router)
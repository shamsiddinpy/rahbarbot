# from aiogram import F
# from aiogram.enums import ContentType
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message
# import os
#
# from apps.bot.button.Inline import personal_info_buttons
# from apps.bot.handler import main_router
# from apps.bot.main import bot
# from apps.bot.state.leader import ComplaintForm
#
#
# @main_router.message(ComplaintForm.waiting_for_attachment, F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO]))
# async def process_file_upload(message: Message, state: FSMContext):
#     file_id = None
#     if message.photo:
#         file_id = message.photo[-1].file_id
#     elif message.video:
#         file_id = message.video.file_id
#
#     if file_id:
#         directory = "attachments"
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#
#         bot_file = await bot.get_file(file_id)
#         file_path = f"{directory}/{bot_file.file_path.split('/')[-1]}"
#         await bot.download_file(bot_file.file_path, destination=file_path)
#         await state.update_data(attachment=file_path)
#
#     await message.answer("O'zingiz haqingizda ma'lumot berasizmi?", reply_markup=personal_info_buttons())
#     await state.set_state(ComplaintForm.waiting_for_user_info)

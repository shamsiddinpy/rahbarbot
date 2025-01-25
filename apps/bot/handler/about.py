# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message
# from telegram import CallbackQuery
# import logging
# from apps.bot.button.Inline import confirm_buttons, get_contact_phone_keyboard
# from apps.bot.handler import main_router
# from apps.bot.state.leader import ComplaintForm
#
#
# @main_router.callback_query(ComplaintForm.waiting_for_user_info, lambda c: c.data in ["provide_info", "skip_info"])
# async def handler_personal_info(callback: CallbackQuery, state: FSMContext):
#     logging.info(f"Callback data: {callback.data}")
#
#     if callback.data == "provide_info":
#         await callback.message.answer("Ismingizni kiriting:")
#         await state.set_state(ComplaintForm.name)
#     elif callback.data == "skip_info":
#         await finalize_data(callback.message, state)
#     await callback.answer()
#
#
# @main_router.message(ComplaintForm.name)
# async def process_name(message: Message, state: FSMContext):
#     full_name = message.text.strip()
#     await state.update_data(full_name=full_name)
#     await message.answer(
#         "Telefon raqamingizni kiriting:",
#         reply_markup=get_contact_phone_keyboard()
#     )
#     await state.set_state(ComplaintForm.phone_number)
#
#
# @main_router.message(ComplaintForm.phone_number)
# async def process_phone_number(message: Message, state: FSMContext):
#     phone_number = message.text.strip()
#     await state.update_data(phone_number=phone_number)
#     await finalize_data(message, state)
#
#
# async def finalize_data(message, state: FSMContext):
#     data = await state.get_data()
#     full_name = data.get("full_name", "Noma'lum")
#     phone_number = data.get("phone_number", "Noma'lum")
#     complaint = data.get("complaint", "Noma'lum")
#
#     summary = (
#         f"Ma'lumotlaringiz:\n\n"
#         f"Ism: {full_name}\n"
#         f"Telefon raqam: {phone_number}\n"
#         f"Murojaat: {complaint}\n\n"
#         f"Hammasi to'g'rimi?"
#     )
#     await message.answer(summary, reply_markup=confirm_buttons())
#     await state.set_state(ComplaintForm.confirm_details)

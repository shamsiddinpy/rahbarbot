from aiogram.fsm.state import StatesGroup, State


class ComplaintForm(StatesGroup):
    waiting_for_complaint = State()
    waiting_for_attachment = State()
    waiting_for_user_info = State()
    name = State()
    phone_number = State()
    confirm_details = State()
    confirming_submission = State()
    waiting_for_reply = State()
